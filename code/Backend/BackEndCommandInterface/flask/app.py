
# File imports
import base64
import json
import sys

import numpy as np
import requests
import websockets
from flask_cors import CORS
from flask_socketio import SocketIO
from google.cloud import storage
import cv2
from pymongo import MongoClient

from flask import Flask, jsonify, request

import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent / 'Backend' / 'ArtGenerationDriver' / 'src'
# print('Backend directory:', backend_dir)
# Add the parent directory to sys.path
sys.path.insert(0, str(backend_dir))
# print('sys.path:', sys.path)

from AGD_Subsystem import AGD_Subsystem
# ********************************************************* INIT SERVER ******************************************
artSubSystem = AGD_Subsystem()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret key'
socketio = SocketIO(app, logger=True)
socketio.run(app, host='wss://websocket-csci2340-78f5f096308b.herokuapp.com', port=443)
CORS(app)

# ********************************************************* DATABASE INIT ****************************************
# Initialize Google Cloud Storage client
storage_client = storage.Client.from_service_account_json('gcp-key.json')
# MongoDB connection 
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]

# ********************************************************* GCP **************************************************
# Route to connect to Google Cloud API
@app.route('/api/google-cloud', methods=['GET', 'POST'])
def google_cloud_api():
    if request.method == 'GET':
        # retrieve list of image_id from DB
        results = collection.find_one({"username": request.args.get('username')})
        return list(results['media'])

    else:
        username, file, filetype = request.args.get('username'), request.files.get('media'), requests.args.get('filetype')
        # Upload the file to Google Cloud Storage
        pub_url = gcs_upload_media(file, filetype)
        if filetype == 'video/mp4':
            # calculate thumbnail
            thumbnail = extract_first_frame(file.stream)
            # upload to gcp
            thumbnail_url = gcs_upload_thumbnail(thumbnail, file) # how to convert from jpg to file
            new_media = (thumbnail_url,pub_url)
        else: 
            new_media = (pub_url,pub_url)

        # check if user exists in db
        user = collection.find_one({'username': username})
        if user is not None:
            # Update user's media field
            collection.update_one({"username": username}, {"$push": {"media": new_media}})

        else:
            # Add new user to the db
            user = {'username': username, 'media': [new_media]}
            collection.insert_one(user)
            
        return jsonify({'message': 'Image uploaded successfully', 'username': username}), 200
    
# function to upload file to GCS
def gcs_upload_media(file : str, type):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.filename.split("/")[-1])
    blob.content_type = type # example: 'image/jpeg'
    blob.upload_from_file(file.stream)
    public_url: str = blob.public_url
    return public_url

# function to upload file to GCS
def gcs_upload_thumbnail(file_stream,file):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.filename.split("/")[-1]+'-thumbnail')
    blob.content_type = type # example: 'image/jpeg'
    blob.upload_from_file(file_stream)
    public_url: str = blob.public_url
    return public_url

def extract_first_frame(mp4_stream):
    # Convert mp4 stream to bytes-like object
    mp4_bytes = mp4_stream.read()
    # Convert bytes-like object to numpy array
    np_array = np.frombuffer(mp4_bytes, np.uint8)
    # Decode video using OpenCV
    video_capture = cv2.VideoCapture()
    video_capture.open(np_array)
    # Check if video capture is successful
    if not video_capture.isOpened():
        raise ValueError("Error: Unable to open video stream.")
    # Read the first frame from the video
    success, frame = video_capture.read()
    # Check if frame is successfully read
    if not success:
        raise ValueError("Error: Unable to read first frame from video.")
    # Release the video capture object
    video_capture.release()
    success, encoded_image = cv2.imencode('.jpg', frame)
    if not success:
        raise ValueError("Error: Unable to encode frame to JPEG format.")
    # Convert encoded image to bytes
    jpeg_bytes = encoded_image.tobytes()

    return jpeg_bytes



@app.route('/api/artGeneration', methods=['GET'])
def artGeneration():
    try:        
        userData = request.json
        modelSelection = userData['modelSelection']
        slider1Value = userData['slider1']
        slider2Value = userData['slider2']
        slider3Value = userData['slider3']

        curLen = len(artSubSystem.generatedOutput)
        artSubSystem.appendGenerationRequest([modelSelection, slider1Value, slider2Value, slider3Value])

        # wait for the art to be generated
        while len(artSubSystem.generatedOutput) == curLen:
            pass

        generatedArtPath = artSubSystem.popleft().pathToOutputData

        requests.post('http://localhost:3000', data=generatedArtPath)

        # upload the generated art to GCS (add caching elements in the future?)
        # gcs_upload_media(generated_art.pathToOutputData, 'video/mp4')
        # gcs_upload_thumbnail(generated_art.pathToOutputData, 'image/jpeg')

        return 'artGenerated'
    
    except Exception as e:
        # app.logger.error('An error occurred: %s', e)
        return f'An error occurred {e}', 500


# API Endpoints that I was using
# MAP_KEY = 'e8aa84fba48bdd97c918f27b26ad74c6'
# request_data = requests.get('https://firms.modaps.eosdis.nasa.gov/api/area/csv/' + MAP_KEY + '/VIIRS_SNPP_NRT/world/1')
# request_data = requests.get('https://www.ncei.noaa.gov/access/services/data/v1?dataset=global-marine&amp;dataTypes=WIND_DIR,WIND_SPEED&amp;stations=AUCE&amp;startDate=2016-01-01&amp;endDate=2016-01-02&amp;boundingBox=90,-180,-90,180')
# get more data from datasets here: https://www.ncei.noaa.gov/access/search/dataset-search?observationTypes=Land%20Surface