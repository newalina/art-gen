##########################################################################
#
# File: BCI_Utils.py
# 
# Purpose of File: The purpose of this file is to contain utility functions
#                   that are used in the Backend Command Interface.
#
# Creation Date: April 30th, 2024
#
# Author: Malique Bodie, David Doan
#       
##########################################################################

# Public Modules
from json import dump
import requests
from google.cloud import storage
from moviepy.editor import VideoFileClip
from PIL import Image
from Backend.BackEndCommandInterface.src.BCI_Definitions import MODEL_RANGES

class BCI_Utils:
    #####################################################################
    # Method:       formatData
    # Purpose:      To format data from API into a list of floats
    # Requirements: N/A
    # Inputs:       dataName - Name of data being fetched from API
    #               data - The data fetched from API
    # Outputs:      ranges - A list containing data ranges for each API  
    #####################################################################
    def formatData(dataName, data):
            out = []
            ranges = []
            if dataName == 'Ocean Temperature':
                result = data['result']
                for key, value in result.items():
                    out.append(float(value))
                ranges.append((min(out),max(out)))
            elif dataName == 'Sea Ice Extent':
                result = data['arcticData']['data']
                for key, value in result.items():
                    out.append(float(value['monthlyMean']))
                ranges.append((min(out),max(out)))
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
                ranges.append((min(out),max(out)))
            return ranges 

    #####################################################################
    # Method:       loadApiData
    # Purpose:      Loads in data from multiple API and writes the 
    #                data to a JSON file.
    # Requirements: N/A
    # Inputs:       apis - A dictionary of API names and URLs
    # Outputs:      apiData -  A dictionary containing the formatted 
    #               data for each API
    #####################################################################
    def loadApiData(apis, outputFile):
        # Dictionary to store data from each API
        apiData = {}

        # Loop through each API URL
        for apiName, apiUrl in apis.items():
            try:
                # Make GET request to API
                response = requests.get(apiUrl)
                data = response.json();  # Extract JSON data from response
                data = BCI_Utils.formatData(apiName, data)
                # Store data in dictionary with URL as key
                apiData[apiName] = data
            except Exception as e:
                print(f"Failed to fetch data from {apiUrl}: {e}")
        return apiData

    #####################################################################
    # Method:       gcsUploadMedia
    # Purpose:      Upload a media file to Google Cloud Storage and
    #                supply callee with URL
    # Requirements: N/A
    # Inputs:       file - Path to the file being uploaded
    #               type - Content type of the file
    # Outputs:      public_url - Public URL of uploaded file.  
    #####################################################################
    def gcsUploadMedia(file, type, storageClient):
        bucket = storageClient.bucket('artgen-storage')
        blob: storage.Blob = bucket.blob(file.split("/")[-1])
        blob.content_type = type 
        blob.upload_from_filename(file)
        publicUrl: str = blob.public_url
        return publicUrl

    #####################################################################
    # Method:       trimVideo
    # Purpose:      Trim a video from specified start time
    # Requirements: N/A
    # Inputs:       inputFile - Path to the input video file
    #               startTime - Start time in seconds for trimming video
    #               duration - Duration in seconds for trimming video
    #               outputFile - Path to save trimmed video
    # Outputs:      None 
    #####################################################################
    def trimVideo(inputFile, startTime, duration, outputFile):
        # Load the video clip
        videoClip = VideoFileClip(inputFile)

        # Trim the video to the specified duration
        #trimmedClip = videoClip.subclip(startTime, startTime + duration)

        # Save the trimmed video
        #trimmedClip.write_videofile(outputFile)
        videoClip.write_videofile(outputFile);

    #####################################################################
    # Method:       generateThumbnail
    # Purpose:      Generate a thumbnail image for a video at a 
    #                specified time
    # Requirements: N/A
    # Inputs:       videoPath - Path to the input video file
    #               outputPath - Path to save generated thumbnail
    #               time - Time in seconds to capture the thumbnail
    # Outputs:      None 
    #####################################################################
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

    def mapValue(value, min_value2, max_value2):
        # Normalize the value to the range [0, 1] based on the first range
        normalized_value = (value) / 99
        
        # Map the normalized value to the second range
        mapped_value = normalized_value * (max_value2 - min_value2) + min_value2
        
        return mapped_value
    
    def mapSliderValue(model_name, values):
        mapped_values = values
        for i, (min,max) in enumerate(MODEL_RANGES[model_name]):
            mapped_values[i] =  BCI_Utils.mapValue(values[i],min,max)
        return mapped_values
