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
import os
import certifi
from flask_cors import CORS
from google.cloud import storage
from pymongo import MongoClient
from flask import Flask, jsonify, request, send_from_directory, url_for
import ffmpeg
import time

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Subsystem import AGD_Subsystem
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging
from Backend.Common.src.CMN_StorageMonitor import CMN_StorageMonitor
from Backend.BackEndCommandInterface.src.BCI_Definitions import BCI_Directories as BCI_DIR
from Backend.BackEndCommandInterface.src.BCI_Definitions import BCI_ErrorCodes as BCI_EC
from Backend.BackEndCommandInterface.src.BCI_Definitions import ENVIRONTMENT_API as BCI_ENV_API
from Backend.BackEndCommandInterface.src.BCI_Utils import BCI_Utils

# ############################# INIT MODULES ############################
# Open the log file
logging = CMN_Logging(CMN_LL.ERR_LEVEL_DEBUG, CMN_LD.CMN_LOG_DOMAIN_BE)
logging.openFile()

# Storage Monitor initialization
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Storage Monitor")
storageMonitor = CMN_StorageMonitor(CMN_DIR.LOGGING_PATH_BASE, AGD_DIR.AGD_DATA_DIR)

# Art Generation Subsystem initialization
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Subsystem")
artSubSystem = AGD_Subsystem(logging)

# ########################### INIT SERVER ################################
# Initialize the art generation ID
ArtGenerationId = -1

# Initialize the Flask app
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Flask Server")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'artgen-secret-key-csci2340'
# Enable CORS to allow requests from the frontend
CORS(app)

logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Server started")

# ############################ DATABASE INIT #############################
# Initialize Google Cloud Storage client
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the Google Cloud Storage Client")
StorageClient = storage.Client.from_service_account_json('gcp-key.json')

# MongoDB connection 
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the MongoDB Client")
Database = MongoClient(BCI_DIR.BCI_MONGO_URI,tlsCAFile=certifi.where()).test # Using test DB 
Collection = Database["product"]

# ########################################################################
# Function:     environmentalDataApi
# Purpose:      Pulls environmental data from various sources, formats the
#               data and sends to front end for slider usage.
# Requirements: N/A
# Inputs:       None
# Outputs:      Json file containing API data, with ranges.
# ########################################################################
@app.route('/api/environmental-data', methods=['GET'])
def environmentalDataApi():
    if request.method == 'GET':
        return jsonify(BCI_Utils.loadApiData(BCI_ENV_API, api_range))

# ########################################################################
# Function:     googleCloudApi
# Purpose:      Uploads media to Google Cloud Storage and updates the user's
#               media field in the database
# Requirements: N/A
# Inputs:       username - the username of the user
#               source - the source of the media
#               isVideo - whether the media is a video or not
#               timestamp - the timestamp of the media
# Outputs:      None, uploads the media to Google Cloud Storage and updates
#               the user's media field in the database
# ########################################################################
@app.route('/api/google-cloud', methods=['GET', 'POST'])
def googleCloudApi():
    if request.method == 'GET':
        # retrieve list of image_id from DB
        results = Collection.find_one({"username": request.args.get('username')})
        if results == None:
            return jsonify({'message': 'User Not Found', 'username': request.args.get('username')})
        return jsonify(results['media'])

    else:
        userName, source, isVideo, timeStamp = request.args.get('username'), request.args.get('source'), int(request.args.get('isVideo')), int(request.args.get('timestamp')) # isVideo: Bool, username: Str, source: Str, timeStamp: int

        # define video and thumbnail files
        videoOutputFileName, thumbnailOutputFileName  = f"{userName}_{int(time.time())}_video.mp4", f"{userName}_{int(time.time())}_thumb.jpg"        

        if(isVideo):
            # trim video
            BCI_Utils.trimVideo(source, timeStamp, 10, videoOutputFileName)
            
            # Upload the trimmed video file to Google Cloud Storage
            videoUrl = BCI_Utils.gcsUploadMedia(videoOutputFileName, 'video/mp4', StorageClient)
            os.remove(videoOutputFileName)

        # generate thumbnail
        BCI_Utils.generateThumbnail(source,thumbnailOutputFileName,timeStamp)

        # Upload the trimmed video file to Google Cloud Storage
        thumbnailUrl = BCI_Utils.gcsUploadMedia(thumbnailOutputFileName, 'image/jpg', StorageClient)
        os.remove(thumbnailOutputFileName)

        if(isVideo):
            # Format MongoDB output
            newMedia = (thumbnailUrl, videoUrl, True) # (thumbnail, video, isVideo)
        else:
            newMedia = (thumbnailUrl, None, False)

        # check if user exists in db
        user = Collection.find_one({'username': userName})
        if user is not None:
            # Update user's media field
            Collection.update_one({"username": userName}, {"$push": {"media": newMedia}})

        else:
            # Add new user to the db
            user = {'username': userName, 'media': [newMedia]}
            Collection.insert_one(user)
            
        return jsonify({'message': 'Media uploaded successfully', 'username': userName}), BCI_EC.BCI_ERR_200

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
@app.route('/api/artGeneration', methods=['GET', 'POST'])
def artGeneration():
    logging.log(CMN_LL.ERR_LEVEL_DEBUG, "BCI_Driver.artGeneration() Art Generation Endpoint requested");

    global ArtGenerationId;
    ArtGenerationId = ArtGenerationId + 1;
    artGenerationId = ArtGenerationId;
    
    try:
        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "BCI_Driver.artGeneration() Getting data from user request");
        modelSelection = slider1Value = slider2Value = slider3Value = slider4Value = slider5Value = slider6Value = 0;
        if request.method == 'GET':
            logging.log(CMN_LL.ERR_LEVEL_DEBUG, "GET request");
            modelSelection = int(request.args.get('modelSelection'));
            slider1Value = int(request.args.get('slider1Value'));
            slider2Value = int(request.args.get('slider2Value'));
            slider3Value = int(request.args.get('slider3Value'));
            slider4Value = int(request.args.get('slider4Value'));
            slider5Value = int(request.args.get('slider5Value'));
            slider6Value = int(request.args.get('slider6Value'));

            logging.log(CMN_LL.ERR_LEVEL_DEBUG, f"BCI_Driver.artGeneration() Model Selection: {modelSelection}, Slider 1: {slider1Value}, Slider 2: {slider2Value}, \
                        Slider 3: {slider3Value}. Slider 4: {slider4Value}, Slider 5: {slider5Value}, Slider 6: {slider6Value}");
        
        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "BCI_Driver.artGeneration() Appending generation request to queue");
        curLen = len(artSubSystem.generatedOutput_);

        artSubSystem.appendGenerationRequest([modelSelection] + BCI_Utils.mapSliderValue(str(modelSelection),[slider1Value, slider2Value, slider3Value, slider4Value, slider5Value, slider6Value]));

        # wait for the art to be generated
        while len(artSubSystem.generatedOutput_) == curLen:
            pass;

        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "BCI_Driver.artGeneration() Art Generation completed");

        ffmpeg.input(AGD_DIR.AGD_OUTPUT_FILE_BASE + str(artGenerationId) + '.mov').output(BCI_DIR.BCI_OUTPUT_FILE_BASE + str(artGenerationId) + '.mp4').overwrite_output().run();
        videoUrl = url_for('getVideo', filename=f'artGenerationOutput_{artGenerationId}.mp4',  _external=True);

        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "BCI_Driver.artGeneration() Art Generation sent to frontend");

        return jsonify({'message': 'Art generated successfully', 'videoUrl': videoUrl}), BCI_EC.BCI_ERR_200;
    except Exception as e:
        logging.log(CMN_LL.ERR_LEVEL_ERROR, f"BCI_Driver.artGeneration() An error occurred {e}");
        return f'An error occurred {e}', BCI_EC.BCI_ERR_500;

##########################################################################
# Function:     getVideo
# Purpose:      Send video data via a URL to the front end
# Requirements: N/A
# Inputs:       fileName - File to be send via URL
# Outputs:      None
##########################################################################
@app.route('/videos/<filename>')
def getVideo(fileName):
    response = send_from_directory(BCI_DIR.BCI_DATA_DIR, fileName, mimetype='video/mp4')
    return response



# Main function wrapper
if __name__ == '__main__':
    app.run(host='10.38.171.41', debug=True)
