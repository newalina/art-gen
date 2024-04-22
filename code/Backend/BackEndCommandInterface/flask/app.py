##########################################################################
#
# File: app.py
# 
# Purpose of File: The purpose of this file is run the server, handle api 
#                   requests to our generation endpoint
#
# Creation Date: March 20th, 2024
#
# Author: David Doan, Alec Pratt, Malique Bodie
#       
##########################################################################
# File imports
import numpy as np
import requests
from flask_cors import CORS
from flask_socketio import SocketIO
from google.cloud import storage
import cv2
from pymongo import MongoClient

from flask import Flask, jsonify, request

# move to a common file eventually
import sys
import os

##########################################################################
# Function:     findTopLevelDirectory
# Purpose:      Find the top level directory of the project
# Requirements: N/A
# Inputs:       startPath - the path to start the search from       
# Outputs:      currentPath - the path to the top level directory
##########################################################################
def findTopLevelDirectory(startPath):
    currentPath = startPath
    while currentPath != os.path.dirname(currentPath):
        if os.path.basename(currentPath) == 'art-gen':
            return currentPath 
    
        currentPath = os.path.dirname(currentPath) 
    return currentPath

currentFilePath = os.path.abspath(__file__)
artGenPath = findTopLevelDirectory(currentFilePath)
sys.path.insert(0, artGenPath)

from projectCode.Backend.ArtGenerationDriver.src import AGD_Subsystem
from projectCode.Backend.Common.src.CMN_ErrorLogging import CMN_LoggingLevels as CMN_LL
from projectCode.Backend.Common.src.CMN_ErrorLogging import log

# Open the log file
log.openFile()

# ########################### INIT SERVER ################################
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Subsystem")
artSubSystem = AGD_Subsystem()
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Subsystem started")

# Initialize the Flask app
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Flask Server")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'artgen-secret-key-csci2340'
socketio = SocketIO(app, logger=True)
socketio.run(app, 
             host='wss://websocket-csci2340-78f5f096308b.herokuapp.com', 
             port=443)

# Enable CORS to allow requests from the frontend
CORS(app)
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Server started")

# ############################ DATABASE INIT #############################
# Initialize Google Cloud Storage client
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Google Cloud Storage Client")
storage_client = storage.Client.from_service_account_json('gcp-key.json')

# MongoDB connection 
log.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the MongoDB Client")
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]

log.log(CMN_LL.ERR_LEVEL_DEBUG, "Database initialized")

# ###############################  GCP ###################################
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


# ######################## ART GENERATION ENDPOINT #######################

##########################################################################
# Function:     artGeneration
# Purpose:      Generate art based on user input, starts an art generation
#               object and waits for the art to be generated
# Requirements: N/A
# Inputs:       modelSelection - the model to be used for generation
#               slider1Value - the value of the first slider
#               slider2Value - the value of the second slider
#               slider3Value - the value of the third slider
#
# Outputs:      None, sends the generated art to the frontend
##########################################################################

@app.route('/api/artGeneration', methods=['GET'])
def artGeneration():
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation Endpoint requested")
    try:
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "Getting user data from request")        
        userData = request.json
        modelSelection = userData['modelSelection']
        slider1Value = userData['slider1']
        slider2Value = userData['slider2']
        slider3Value = userData['slider3']
        
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "Appending generation request to queue")
        curLen = len(artSubSystem.generatedOutput)
        artSubSystem.appendGenerationRequest([modelSelection, slider1Value, slider2Value, slider3Value])

        # wait for the art to be generated
        while len(artSubSystem.generatedOutput) == curLen:
            pass
        
        generatedArtPath = artSubSystem.popleft().pathToOutputData
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation completed")

        requests.post('http://localhost:3000', data=generatedArtPath)

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation sent to frontend")
        # upload the generated art to GCS (add caching elements in the future?)
        # gcs_upload_media(generated_art.pathToOutputData, 'video/mp4')
        # gcs_upload_thumbnail(generated_art.pathToOutputData, 'image/jpeg')
        return 'artGenerated'
    
    except Exception as e:
        log.log(CMN_LL.ERR_LEVEL_ERROR, f"An error occurred {e}")
        return f'An error occurred {e}', 500