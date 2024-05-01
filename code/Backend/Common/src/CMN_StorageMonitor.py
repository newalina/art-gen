##########################################################################
#
# File: AGD_Definitions.py
# 
# Purpose of File: The purpose of this file is to maintain storage levels
#                   on the host machine so that there are not too many
#                   files saved to disk and consuming valuable memory
#                   resources.
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt, David Doan
#       
##########################################################################

# TODO: Complete this file. As of now, it may not be functional .

# Public Modules
import threading
import os
import time

class CMN_StorageMonitor:

    def __init__(self, errorLogDirectory, artDataDirectory):
        # Define a maximum number of files allowed
        self.maxFiles_ = 10;

        self.errorLogDirectory_ = errorLogDirectory;
        self.artDataDirectory_ = artDataDirectory;
    
        self.monitorDebugThread_ = threading.Thread(target=self.monitorDebugLogDirectory);
        self.monitorDebugThread_.start();

    def monitorDebugLogDirectory(self):
        while True:  # Infinite loop to continuously check the directory
            self.checkAndCleanDirectory()
            self.checkAndCleanArtDirectory()
            time.sleep(60)  # Wait for 60 seconds before checking again

    def checkAndCleanDirectory(self): 
        if (len(os.listdir(self.errorLogDirectory_)) == 0):
            return       
        # Get a list of all files in the directory sorted by creation time (oldest first)
        files = sorted(
            (os.path.join(self.errorLogDirectory_, f) for f in os.listdir(self.errorLogDirectory_)),
            key=lambda f: os.path.getctime(f)
        )

        # If the number of files exceeds the maximum, remove the oldest ones
        while len(files) > 1 and len(files) > self.maxFiles_:
            os.remove(files[0])
            print(f"Removed {files[0]} due to excess in file count")
            files.pop(0)  # Remove the file from the list once deleted

    def checkAndCleanArtDirectory(self):       
        if (len(os.listdir(self.artDataDirectory_)) == 0):
            return
        # Get a list of all files in the directory sorted by id (oldest first) artGeneration_id.mov
        files = sorted(
            (os.path.join(self.artDataDirectory_, f) for f in os.listdir(self.artDataDirectory_)),
            key=lambda f: int(f.split('_')[1].split(".")[0]) if len(f.split('_')) == 2 else 0
        )

        # If the number of files exceeds the maximum, remove the oldest ones
        while len(files) > 1 and len(files) > self.maxFiles_:
            os.remove(files[0])
            print(f"Removed {files[0]} due to excess in file count")
            files.pop(0)