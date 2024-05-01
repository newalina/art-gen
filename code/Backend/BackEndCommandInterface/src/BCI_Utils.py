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

    environmental_apis = {
        'Carbon Dioxide' : 'https://global-warming.org/api/co2-api',
        'Methane' : 'https://global-warming.org/api/methane-api',
        'Nitrous Oxide' : 'https://global-warming.org/api/nitrous-oxide-api',
        'Ocean Temperature' : 'https://global-warming.org/api/ocean-warming-api'
    }

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


    # ##################################################################################################################
    # Function: load_api_data
    # Purpose: This function loads data from multiple APIs and writes it to a JSON file
    # Parameters:
    #   apis (dict): A dictionary of API names and URLs
    #   output_file (str): The path to the output JSON file
    # Returns:
    #   None
    # ##################################################################################################################
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
    def gcs_upload_media(file, type):
        bucket = storage_client.bucket('artgen-storage')
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
    def trim_video(input_file, start_time, duration, output_file):
        # Load the video clip
        video_clip = VideoFileClip(input_file)

        # Trim the video to the specified duration
        trimmed_clip = video_clip.subclip(start_time, start_time + duration)

        # Save the trimmed video
        trimmed_clip.write_videofile(output_file)

    # ##################################################################################################################
    # Generate a thumbnail image for a video at the specified time.

    # Parameters:
    #     video_path (str): The path to the input video file.
    #     output_path (str): The path to save the generated thumbnail image.
    #     time (float): The time in seconds at which to capture the thumbnail.

    # Returns:
    #     None
    # ##################################################################################################################
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

    # ********************************************************* API FUNCS **************************************************