# #########################################################################

# File: app.py

# Purpose of File: The purpose of this file is run the server, handle api 
#                   requests to our generation endpoint

# Creation Date: March 20th, 2024

# Author: David Doan, Alec Pratt, Malique Bodie
      
# #########################################################################

# Public Modules
from flask_cors import CORS
from google.cloud import storage
from pymongo import MongoClient
from flask import Flask, jsonify, request, send_from_directory, url_for
import ffmpeg

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Subsystem import AGD_Subsystem
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging
from Backend.Common.src.CMN_StorageMonitor import CMN_StorageMonitor
from Backend.BackEndCommandInterface.src.BCI_Definitions import BCI_Directories as BCI_DIR
from Backend.BackEndCommandInterface.src.BCI_Utils import BCI_Utils
# from BCI_Utils import BCI_Utils

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
ART_GENERATION_ID = -1

def get_next_art_generation_id():
    global ART_GENERATION_ID
    ART_GENERATION_ID += 1
    return ART_GENERATION_ID

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
storage_client = storage.Client.from_service_account_json('gcp-key.json')

# MongoDB connection 
logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Starting the MongoDB Client")
MONGO_URI = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'
db = MongoClient(MONGO_URI).test # Using test DB 
collection = db["product"]

# ###############################  GCP ###################################

# Route to connect to Google Cloud API
# ########################################################################
# Function:     google_cloud_api
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
        BCI_Utils.trim_video(source,timestamp,10,video_output_filename)
        
        # Upload the trimmed video file to Google Cloud Storage
        video_url = BCI_Utils.gcs_upload_media(video_output_filename, 'video/mp4')

        # generate thumbnail
        BCI_Utils.generate_thumbnail(source,thumbnail_output_filename,timestamp)

        # Upload the trimmed video file to Google Cloud Storage
        thumbnail_url = BCI_Utils.gcs_upload_media(thumbnail_output_filename, 'image/jpg')

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
        if request.method == 'POST':
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

        # artSubSystem.appendGenerationRequest([modelSelection, slider1Value, slider2Value, slider3Value, slider4Value, slider5Value, slider6Value])

        # # wait for the art to be generated
        # while len(artSubSystem.generatedOutput_) == curLen:
        #     pass

        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation completed")

        ffmpeg.input(AGD_DIR.AGD_OUTPUT_FILE_BASE + str(artGenerationId) + '.mov').output(BCI_DIR.BCI_OUTPUT_FILE_BASE + str(artGenerationId) + '.mp4').overwrite_output().run()
        videoUrl = url_for('get_video', filename=f'artGenerationOutput_{artGenerationId}.mp4',  _external=True)

        logging.log(CMN_LL.ERR_LEVEL_DEBUG, "Art Generation sent to frontend")

        return jsonify({'message': 'Art generated successfully', 'videoUrl': videoUrl}), 200
    except Exception as e:
        logging.log(CMN_LL.ERR_LEVEL_ERROR, f"An error occurred {e}")
        return f'An error occurred {e}', 500

# host the videos as urls
@app.route('/videos/<filename>')
def get_video(filename):
    response = send_from_directory(BCI_DIR.BCI_DATA_DIR, filename, mimetype='video/mp4')
    return response
    
if __name__ == '__main__':
    app.run(host='10.38.171.41', debug=True)