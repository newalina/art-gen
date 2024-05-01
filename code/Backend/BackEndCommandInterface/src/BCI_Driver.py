##########################################################################
#
# File: BCI_Driver.py
# 
# Purpose of File: The purpose of this file is run the server, handle api 
#                   requests to our generation endpoint
#
# Creation Date: March 20th, 2024
#
# Author: David Doan, Alec Pratt, Malique Bodie
#       
##########################################################################

# Public Modules
import requests
from flask_cors import CORS
from flask_socketio import SocketIO
from google.cloud import storage
from pymongo import MongoClient
from moviepy.editor import VideoFileClip
from PIL import Image
import json
from flask import Flask, jsonify, request, send_file, send_from_directory, url_for
import ffmpeg
import sys

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Subsystem import AGD_Subsystem
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging
from Backend.Common.src.CMN_StorageMonitor import CMN_StorageMonitor
from Backend.BackEndCommandInterface.src.BCI_Definitions import BCI_Directories as BCI_DIR

# Open the log file
logging = CMN_Logging(CMN_LL.ERR_LEVEL_DEBUG, CMN_LD.CMN_LOG_DOMAIN_BE)
logging.openFile()

# Storage Monitor initialization
storageMonitor = CMN_StorageMonitor(CMN_DIR.LOGGING_PATH_BASE, AGD_DIR.AGD_DATA_DIR)

# ########################### INIT SERVER ################################
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Subsystem")
artSubSystem = AGD_Subsystem(logging)
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Subsystem started")

ART_GENERATION_ID = -1

# Initialize the Flask app
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Flask Server")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'artgen-secret-key-csci2340'
socketio = SocketIO(app, logger=True)
socketio.run(app, 
             host='wss://websocket-csci2340-78f5f096308b.herokuapp.com', 
             port=443)

# Enable CORS to allow requests from the frontend
CORS(app)

logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Server started")

# ############################ DATABASE INIT #############################
# Initialize Google Cloud Storage client
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Google Cloud Storage Client")
storage_client = storage.Client.from_service_account_json('gcp-key.json')

# MongoDB connection 
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the MongoDB Client")
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]

logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Database initialized")

# ********************************************************* API DATA INIT **************************************************
environmental_apis = {
    'Carbon Dioxide' : 'https://global-warming.org/api/co2-api',
    'Methane' : 'https://global-warming.org/api/methane-api',
    'Nitrous Oxide' : 'https://global-warming.org/api/nitrous-oxide-api',
    'Ocean Temperature' : 'https://global-warming.org/api/ocean-warming-api'
}

def format_data(data_name, data):
        out = []
        if data_name == 'Ocean Temperature':
            result = data['result']
            for key, value in result.items():
                out.append(float(value))
        else:
            if data_name == 'Carbon Dioxide':
                key = 'co2'
            elif data_name == 'Methane':
                key = 'methane'
            elif data_name == 'Nitrous Oxide':
                key = 'nitrous'
            result = data[key]
            for dict in result:
                out.append(float(dict['trend']))
        return out  

# load environmental data
def load_api_data(apis, output_file):
    # Dictionary to store data from each API
    api_data = {}

    # Loop through each API URL
    for api_name, api_url in apis.items():
        try:
            # Make GET request to API
            response = requests.get(api_url)
            data = response.json()  # Extract JSON data from response
            data = format_data(api_name, data)
            # Store data in dictionary with URL as key
            api_data[api_name] = data
        except Exception as e:
            print(f"Failed to fetch data from {api_url}: {e}")

    # Write API data to JSON file
    with open(output_file, 'w') as f:
        json.dump(api_data, f, indent=4)

# ###############################  GCP ###################################
# Route to connect to Google Cloud API
@app.route('/api/google-cloud', methods=['GET', 'POST'])
def google_cloud_api():
    if request.method == 'GET':
        # retrieve list of image_id from DB
        results = collection.find_one({"username": request.args.get('username')})
        return list(results['media'])

    else:
        username, source, isVideo, timestamp = request.args.get('username'), request.args.get('source'), bool(request.args.get('isVideo')), int(request.args.get('timestamp')) # isVideo: Bool, username: Str, source: Str, timeStamp: int
        
        # define video and thumbnail files
        video_output_filename, thumbnail_output_filename  = "trimmed_video.mp4","thumbnail.jpg"        
        
        # trim video
        trim_video(source,timestamp,10,video_output_filename)
        
        # Upload the trimmed video file to Google Cloud Storage
        video_url = gcs_upload_media(video_output_filename, 'video/mp4')

        # generate thumbnail
        generate_thumbnail(source,thumbnail_output_filename,timestamp)

        # Upload the trimmed video file to Google Cloud Storage
        thumbnail_url = gcs_upload_media(thumbnail_output_filename, 'image/jpg')

        # Format MongoDB output
        new_media = (thumbnail_url,video_url,isVideo) # (thumbnail, video, is_video)

        # check if user exists in db
        user = collection.find_one({'username': username})
        if user is not None:
            # Update user's media field
            collection.update_one({"username": username}, {"$push": {"media": new_media}})

        else:
            # Add new user to the db
            user = {'username': username, 'media': [new_media]}
            collection.insert_one(user)
            
        return jsonify({'message': 'Media uploaded successfully', 'username': username}), 200
   
    
"""
Uploads a media file to Google Cloud Storage and returns its public URL.

Parameters:
    file (str): The path to the file to be uploaded.
    type (str): The content type of the file (e.g., 'image/jpeg').

Returns:
    str: The public URL of the uploaded file.
"""
def gcs_upload_media(file, type):
    bucket = storage_client.bucket('artgen-storage')
    blob: storage.Blob = bucket.blob(file.split("/")[-1])
    blob.content_type = type 
    blob.upload_from_filename(file)
    public_url: str = blob.public_url
    return public_url

"""
Trim a video from the specified start time to the end time and save it to the output path.

Parameters:
    input_file (str): The path to the input video file.
    start_time (float): The start time in seconds for trimming the video.
    duration (float): The duration in seconds for trimming the video.
    output_file (str): The path to save the trimmed video.

    Returns:
        None
"""
def trim_video(input_file, start_time, duration, output_file):
    # Load the video clip
    video_clip = VideoFileClip(input_file)

    # Trim the video to the specified duration
    trimmed_clip = video_clip.subclip(start_time, start_time + duration)

    # Save the trimmed video
    trimmed_clip.write_videofile(output_file)

"""
Generate a thumbnail image for a video at the specified time.

Parameters:
    video_path (str): The path to the input video file.
    output_path (str): The path to save the generated thumbnail image.
    time (float): The time in seconds at which to capture the thumbnail.

Returns:
    None
"""
def generate_thumbnail(video_path, output_path, time):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Capture a frame at the specified time
    thumbnail = video_clip.get_frame(time)

    # Convert frame (numpy array) to image
    thumbnail = Image.fromarray(thumbnail)

    # Save the thumbnail image
    thumbnail.save(output_path)

    # Close the video clip
    video_clip.close()


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

# Helper function to increment and get the current ART_GENERATION_ID
def get_next_art_generation_id():
    global ART_GENERATION_ID
    ART_GENERATION_ID += 1
    return ART_GENERATION_ID

def convert_mov_to_mp4(input_path, output_path):
    ret = ffmpeg.input(input_path).output(output_path).overwrite_output().run()
    print(ret);

@app.route('/api/artGeneration', methods=['GET', 'POST'])
def artGeneration():
    logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation Endpoint requested")
    artGenerationId = get_next_art_generation_id()
    
    try:
        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Getting user data from request")  
        modelSelection = slider1Value = slider2Value = slider3Value = slider4Value = slider5Value = slider6Value = 0
        if request.method == 'GET':
            logging.log(CMN_LL.ERR_LEVEL_DEBUG, "GET request")
            modelSelection = int(request.args.get('modelSelection'))
            slider1Value = int(request.args.get('slider1Value'))
            slider2Value = int(request.args.get('slider2Value'))
            slider3Value = int(request.args.get('slider3Value'))
            slider4Value = int(request.args.get('slider4Value'))
            slider5Value = int(request.args.get('slider5Value'))
            slider6Value = int(request.args.get('slider6Value'))

            logging.log(CMN_LL.ERR_LEVEL_DEBUG, f"Model Selection: {modelSelection}, Slider 1: {slider1Value}, Slider 2: {slider2Value}, Slider 3: {slider3Value}. Slider 4: {slider4Value}, Slider 5: {slider5Value}, Slider 6: {slider6Value}")
        
        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Appending generation request to queue")
        curLen = len(artSubSystem.generatedOutput_)

        # to work with TouchDesigner Potentially, @Alec
        artSubSystem.appendGenerationRequest([modelSelection, slider1Value, slider2Value, slider3Value, slider4Value, slider5Value, slider6Value])

        # wait for the art to be generated
        while len(artSubSystem.generatedOutput_) == curLen:
            pass

        # generatedArtPath = artSubSystem.generatedOutput_.popleft().pathToOutputData
        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation completed")

        print(AGD_DIR.AGD_OUTPUT_FILE_BASE + str(artGenerationId) + '.mov')
        print(BCI_DIR.BCI_OUTPUT_FILE_BASE + str(artGenerationId) + '.mp4')
        convert_mov_to_mp4(AGD_DIR.AGD_OUTPUT_FILE_BASE + str(artGenerationId) + '.mov', BCI_DIR.BCI_OUTPUT_FILE_BASE + str(artGenerationId) + '.mp4')
        videoUrl = url_for('get_video', filename=f'artGenerationOutput_{artGenerationId}.mp4',  _external=True)

        # old method of sending data directly to frontend
        # filePath = f'{artGenPath}/Backend/ArtGenerationDriver/data/artGenerationOutput_{artGenerationId}.mov'

        # with open(filePath, 'rb') as f:
        #     # file = {'file': (filePath, f, 'video/mp4')}
        #     # requests.post('http://localhost:3000', files=file)
        
        # requests.post('http://localhost:3000', data=videoUrl)

        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation sent to frontend")

        # return send_file(artGenPath + f'/Backend/ArtGenerationDriver/data/artGenerationOutput_{artGenerationId}.mov', mimetype='video/mp4')
        return jsonify({'message': 'Art generated successfully', 'videoUrl': videoUrl}), 200
    except Exception as e:
        logging.log(CMN_LL.ERR_LEVEL_ERROR, f"An error occurred {e}")
        return f'An error occurred {e}', 500

# host the videos as urls
@app.route('/videos/<filename>')
def get_video(filename):
    response = send_from_directory(BCI_DIR.BCI_DATA_DIR, filename, mimetype='video/mp4', as_attachment=True)
    response.headers['Content-Type'] = 'video/mp4;'
    response.headers['Accept-Ranges'] = 'bytes' 
    response.headers['Content-Disposition'] = 'inline; filename="{}"'.format(filename)
    return response
    
if __name__ == '__main__':
    app.run(host='10.38.171.41', debug=True)
    #storageMonitor.stop()
    #logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Server closed")
    #logging.closeFile()
    #sys.exit(0)