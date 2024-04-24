##########################################################################
#
# File: CMN_StorageMonitor.py
# 
# Purpose of File: TODO: Fill in the purpose of this file
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
# Modifiers: David Doan
#       
##########################################################################
from enum import IntEnum
import threading
import os
import time

class CMN_StorageMonitorErrorCode(IntEnum):
    SM_ERROR_CODE_OK = 0
    SM_ERROR_CODE_FULL = 0


class CMN_StorageMonitor:

    def __init__(self, errorLogDirectory, artDataDirectory):

        self.errorLogDirectory = errorLogDirectory;
        self.artDataDirectory = artDataDirectory;
    
        self.monitorDebugThread = threading.Thread(target=self.monitorDebugLogDirectory);

    def monitorDebugLogDirectory(self):
        while True:  # Infinite loop to continuously check the directory
            self.check_and_clean_directory()
            self.check_and_clean_art_directory()
            time.sleep(60)  # Wait for 60 seconds before checking again

    def check_and_clean_directory(self):
        # Define a maximum number of files allowed
        max_files = 10
        
        # Get a list of all files in the directory sorted by creation time (oldest first)
        files = sorted(
            (os.path.join(self.errorLogDirectory, f) for f in os.listdir(self.errorLogDirectory)),
            key=lambda f: os.path.getctime(f)
        )

        # If the number of files exceeds the maximum, remove the oldest ones
        while len(files) > max_files:
            os.remove(files[0])
            print(f"Removed {files[0]} due to excess in file count")
            files.pop(0)  # Remove the file from the list once deleted

    def check_and_clean_art_directory(self):
        # Define a maximum number of files allowed
        max_files = 10
        
        # Get a list of all files in the directory sorted by id (oldest first) artGeneration_id.mov
        files = sorted(
            (os.path.join(self.artDataDirectory, f) for f in os.listdir(self.artDataDirectory)),
            key=lambda f: int(f.split('_')[0])
        )

        # If the number of files exceeds the maximum, remove the oldest ones
        while len(files) > max_files:
            os.remove(files[0])
            print(f"Removed {files[0]} due to excess in file count")
            files.pop(0)