##########################################################################
#
# File: CMN_ErrorLogging.py
# 
# Purpose of File: The purpose of this file is to contain all of the 
#                   logging functionality required by the Art Generator
#                   Project including definitions and classes.
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
from enum import IntEnum
import sys
import os
from datetime import datetime

#from AGD_Definitions import AGD_Directories as AGD_DIR
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
        if os.path.basename(currentPath) == 'code':
            return currentPath 
    
        currentPath = os.path.dirname(currentPath) 
    return currentPath

currentFilePath = os.path.abspath(__file__)
artGenPath = findTopLevelDirectory(currentFilePath)
sys.path.insert(0, artGenPath)

# CLass Definitions
class CMN_Logging:

    #####################################################################
    # Function:     __init__
    # Purpose:      Initialize a new instance of the CMN_Logging class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self, threshold):
        # Need to generalize this path to be system independent. 
        # self.path = "c:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\Common\\logs\\" + self.createTime(self.getTime()) + "_runLog.log";
        # self.path = artGenPath + "\\Common\\" + self.createTime(self.getTime()) + "_runLog.log";
        # print(artGenPath);
        # self.path = f'{artGenPath}\Backend\Common\debugLog\{self.createTime(self.getTime())}_runLog.log';
        self.path = os.path.join(artGenPath, "Backend", "Common", "debugLog", f'{self.createTime(self.getTime())}_runLog.log');
        self.threshold = threshold;
        self.file = None;

        self.prepend = [", ERROR: ", ", WARNING: ", ", DEBUG: "," TRACE:" ]; 

    #####################################################################
    # Function:     getTime
    # Purpose:      Get the current time
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def getTime(self):
        return datetime.now();

    #####################################################################
    # Function:     createTime
    # Purpose:      Format the time to be used for a filename
    # Requirements: N/A
    # Inputs:       self - current class member    
    #               time - The time to be formatted    
    # Outputs:      None  
    #####################################################################
    def createTime(self, time):
        return str(time.year) + '-' + f"{time.month:02}" + '-' + f"{time.day:02}" + '-' \
            + f"{time.hour:02}" + '.' + f"{time.minute:02}" + '.' + f"{time.second:02}" + '.' + str(time.microsecond);

    #####################################################################
    # Function:     log
    # Purpose:      Log a message to file
    # Requirements: N/A
    # Inputs:       self - current class member    
    #               level - Logging level of input message
    #               message - Message to be logged
    # Outputs:      None  
    #####################################################################
    def log(self, level, message):
        if(level <= self.threshold):
            # Create string to write to file
            # Want the date, error level, message
            logString = str(self.getTime()) + self.prepend[level] + message + "\n";

            self.file.write(logString);
        return

    #####################################################################
    # Function:     openFile
    # Purpose:      Open file to write to
    # Requirements: N/A
    # Inputs:       self - current class member    
    # Outputs:      None  
    #####################################################################
    def openFile(self):
        self.file = open(self.path, "w");

    #####################################################################
    # Function:     closeFile
    # Purpose:      Close file that is being written to
    # Requirements: N/A
    # Inputs:       self - current class member    
    # Outputs:      None  
    #####################################################################
    def closeFile(self):
        self.file.close();


#####################################################################
# Enum:         CMN_LoggingLevels
# Enum Type:    IntEnum
# Description:  This enum contains the logging levels that can be 
#                used in the Art Generator Project. Review the 
#                guide to learn about how to use these logging 
#                levels. 
# Values:
#   ERR_LEVEL_ERROR - Error Logging Level
#   ERR_LEVEL_WARNING - Warning Logging Level
#   ERR_LEVEL_DEBUG - Debug Logging Level
#   ERR_LEVEL_TRACE - Trace Logging Level
#   ERR_LEVEL_ALL - Logging level enabling all logging.              
#####################################################################
class CMN_LoggingLevels(IntEnum):
    ERR_LEVEL_ERROR     = 0
    ERR_LEVEL_WARNING   = 1
    ERR_LEVEL_DEBUG     = 2
    ERR_LEVEL_TRACE     = 3
    ERR_LEVEL_ALL       = 4 


# Instance of CMN_Logging Class to be used. 
# log = CMN_Logging(CMN_LoggingLevels.ERR_LEVEL_ALL);
