# ####################################################################################################
# File: BCI_Utils.py
#
# Purpose of File: The purpose of this file is to contain utility functions
#                     that are used in the Backend Command Interface.
#
# Creation Date: April 20th, 2024
#
# Author: Malique Bodie, David Doan
# ####################################################################################################

# Public Modules
import json
import requests
from google.cloud import storage
from moviepy.editor import VideoFileClip
from PIL import Image

class BCI_Utils:
    # ********************************************************* API DATA INIT **************************************************

    # ##################################################################################################################
    # Function: format_data
    # Purpose: This function formats the data from the API into a list of floats
    # Parameters:
    #   data_name (str): The name of the data being fetched from the API
    #   data (dict): The data fetched from the API
    # Returns:
    #   list: A list of floats containing the formatted data
    # ##################################################################################################################

    def formatData(dataName, data):
            out = []
            if dataName == 'Ocean Temperature':
                result = data['result']
                for key, value in result.items():
                    out.append(float(value))
            else:
                if dataName == 'Carbon Dioxide':
                    key = 'co2'
                elif dataName == 'Methane':
                    key = 'methane'
                elif dataName == 'Nitrous Oxide':
                    key = 'nitrous'
                result = data[key]
                for dict in result:
                    out.append(float(dict['trend']))
            return out  


    # ##################################################################################################################
    # Function: load_api_data
    # Purpose: This function loads data from multiple APIs and writes it to a JSON file
    # Parameters:
    #   apis (dict): A dictionary of API names and URLs
    #   output_file (str): The path to the output JSON file
    # Returns:
    #   None
    # ##################################################################################################################
    def loadApiData(apis, outputFile):
        # Dictionary to store data from each API
        apiData = {}

        # Loop through each API URL
        for apiName, apiUrl in apis.items():
            try:
                # Make GET request to API
                response = requests.get(apiUrl)
                data = response.json()  # Extract JSON data from response
                data = BCI_Utils.formatData(apiName, data)
                # Store data in dictionary with URL as key
                apiData[apiName] = data
            except Exception as e:
                print(f"Failed to fetch data from {apiUrl}: {e}")

        # Write API data to JSON file
        with open(outputFile, 'w') as f:
            json.dump(apiData, f, indent=4)


    # ********************************************************* DATABASE FUNCS **************************************************

    # ##################################################################################################################
    # Uploads a media file to Google Cloud Storage and returns its public URL.
    #
    # Parameters:
    #     file (str): The path to the file to be uploaded.
    #     type (str): The content type of the file (e.g., 'image/jpeg').
    #
    # Returns:
    #     str: The public URL of the uploaded file.
    # ##################################################################################################################
    def gcsUploadMedia(file, type, storageClient):
        bucket = storageClient.bucket('artgen-storage')
        blob: storage.Blob = bucket.blob(file.split("/")[-1])
        blob.content_type = type 
        blob.upload_from_filename(file)
        public_url: str = blob.public_url
        return public_url

    # ##################################################################################################################
    # Trim a video from the specified start time to the end time and save it to the output path.

    # Parameters:
    #     input_file (str): The path to the input video file.
    #     start_time (float): The start time in seconds for trimming the video.
    #     duration (float): The duration in seconds for trimming the video.
    #     output_file (str): The path to save the trimmed video.

    #     Returns:
    #         None
    # ##################################################################################################################
    def trimVideo(inputFile, startTime, duration, outputFile):
        # Load the video clip
        videoClip = VideoFileClip(inputFile)

        # Trim the video to the specified duration
        trimmedClip = videoClip.subclip(startTime, startTime + duration)

        # Save the trimmed video
        trimmedClip.write_videofile(outputFile)

    # ##################################################################################################################
    # Generate a thumbnail image for a video at the specified time.

    # Parameters:
    #     video_path (str): The path to the input video file.
    #     output_path (str): The path to save the generated thumbnail image.
    #     time (float): The time in seconds at which to capture the thumbnail.

    # Returns:
    #     None
    # ##################################################################################################################
    def generateThumbnail(videoPath, outputPath, time):
        # Load the video clip
        videoClip = VideoFileClip(videoPath)

        # Capture a frame at the specified time
        thumbnail = videoClip.get_frame(time)

        # Convert frame (numpy array) to image
        thumbnail = Image.fromarray(thumbnail)

        # Save the thumbnail image
        thumbnail.save(outputPath)

        # Close the video clip
        videoClip.close()

    # ********************************************************* API FUNCS **************************************************