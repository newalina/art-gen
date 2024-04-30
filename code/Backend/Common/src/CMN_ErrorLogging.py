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

from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
# from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
# CLass Definitions
class CMN_Logging:

    #####################################################################
    # Method:     __init__
    # Purpose:      Initialize a new instance of the CMN_Logging class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self, threshold, domain):

        if(domain == CMN_LD.CMN_LOG_DOMAIN_BE):
            # Global Logging for Backend / AGD
            self.path_ = str(CMN_DIR.LOGGING_PATH_BASE) + "backend_runLog_" + ".log";
        elif(domain == CMN_LD.CMN_LOG_DOMAIN_TD):
            # Logging for Touch Designer
            self.path_ = str(CMN_DIR.LOGGING_PATH_BASE) + "touch_designer_runLog_" + self.createTime(self.getTime()) + ".log";
        elif(domain == CMN_LD.CMN_LOG_DOMAIN_UT):
            # Logging for Unit Tests
            self.path_ = str(CMN_DIR.LOGGING_PATH_BASE_UT) + "unit_test_runLog_" + self.createTime(self.getTime()) + ".log";
        else:
            print("ERROR");
        
        self.threshold_ = threshold;
        self.file_ = None;
               
        # This could be moved 
        self.prepend = [", ERROR: ", ", WARNING: ", ", DEBUG: "," TRACE:" ]; 

    #####################################################################
    # Method:     getTime
    # Purpose:      Get the current time
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def getTime(self):
        return datetime.now();

    #####################################################################
    # Method:     createTime
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
    # Method:     log
    # Purpose:      Log a message to file
    # Requirements: N/A
    # Inputs:       self - current class member    
    #               level - Logging level of input message
    #               message - Message to be logged
    # Outputs:      None  
    #####################################################################
    def log(self, level, message):
        if(level <= self.threshold_):
            # Create string to write to file
            # Want the date, error level, message
            logString = str(self.getTime()) + self.prepend[level] + message + "\n";

            self.file_.write(logString);
        return

    #####################################################################
    # Method:     openFile
    # Purpose:      Open file to write to
    # Requirements: N/A
    # Inputs:       self - current class member    
    # Outputs:      None  
    #####################################################################
    def openFile(self):
        self.file_ = open(self.path_, "w");

    #####################################################################
    # Method:     closeFile
    # Purpose:      Close file that is being written to
    # Requirements: N/A
    # Inputs:       self - current class member    
    # Outputs:      None  
    #####################################################################
    def closeFile(self):
        self.file_.close();



# Instance of CMN_Logging Class to be used. 
# log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_BE);
