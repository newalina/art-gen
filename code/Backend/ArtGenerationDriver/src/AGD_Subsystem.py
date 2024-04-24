##########################################################################
#
# File: AGD_Subsystem.py
# 
# Purpose of File: The purpose of this file is to contain the Art
#                   Generation Driver Subsystem class. This class is 
#                   responsible for controlling the entirety of the
#                   Touch Designer interface, generating art, and
#                   returning art to the user.
#
# Creation Date: April 14th, 2024
#
# Author: David Doan, Alec Pratt
#       
##########################################################################

# Public Modules
import sys
import threading
from collections import deque
import logging
import os

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Definitions as AGD_DEF;
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_ErrorLogging import log

##########################################################################
#
# Class: AGD_Subsystem
#
# Purpose: The purpose of this class is to contain the Art Generation
#           Driver Subsystem class. This class is responsible for
#           controlling the entirety of the Touch Designer interface,
#           generating art, and returning art to the user.
#
##########################################################################
class AGD_Subsystem:

    #####################################################################
    # Method:       __init__
    # Purpose:      Initialize a new instance of the AGD_Subsystem class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self, logger):
        # expects a list of [modelSelection, param1, param2, param3]
        self.generationQueue_ = deque();
        self.generatedOutput_ = deque();
        self.logger = logger;

        # init a thread to handle the generation queue
        self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.__init__: Starting Generation Thread");
        self.generationThread_ = threading.Thread(target=self.processGenerationQueue);

    #####################################################################
    # Method:       appendGenerationRequest
    # Purpose:      Add an AGD_ArtGeneratorUnit object to the queue for
    #                processing in Touch Designer
    # Requirements: N/A
    # Inputs:       self - current class member     
    #               object - The AGD_ArtGeneratorUnit to be appended for
    #                art generation.  
    # Outputs:      
    #####################################################################
    def appendGenerationRequest(self, object) -> int:

        if( len(self.generationQueue) >= AGD_DEF.MAX_QUEUE_SIZE.value ):
            self.logger.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_Subsystem.appendGenerationRequest: Queue is Full");
            return -1;
        else:
            self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.appendGenerationRequest: Appending Generation Request");
            self.generationQueue_.append(object);
        
        return 0;

    #####################################################################
    # Method:       popGenerationRequest
    # Purpose:      Remove an AGD_ArtGeneratorUnit object from the queue 
    #                after it has completed processing
    # Requirements: N/A
    # Inputs:       self - current class member     
    # Outputs:      
    #####################################################################
    def popGenerationRequest(self):
        self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.popGenerationRequest: Popping Generation Request");
        return self.generationQueue_.popleft();

    #####################################################################
    # Method:       checkIfFileExists
    # Purpose:      Determine if art generation output file has been
    #                written.
    # Requirements: N/A
    # Inputs:       self - current class member 
    #               path - path to the expected art generation output file    
    # Outputs:      boolean - True if file is found, false if not found  
    #####################################################################
    def checkIfFileExists(self, path):
        self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.checkIfFileExists: Checking if File Exists");
        return os.path.isfile(path);

    #####################################################################
    # Method:       processGenerationQueue
    # Purpose:      Driving function for the Art Generator Driver that
    #                handles the processing of the request queue. 
    # Requirements: N/A
    # Inputs:       self - current class member  
    # Outputs:      None
    #####################################################################
    def processGenerationQueue(self):
        while(True):
            if( len(self.generationQueue_) > 0 ):
                self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.processGenerationQueue: Processing Generation Queue");
                a, param1, param2, param3 = self.popGenerationRequest();
                artGenerator = AGD_ArtGeneratorUnit(a, param1, param2, param3);
                artGenerator.writeToJSON();
                artGenerator.startTouchDesigner();

                # check if the file exists
                while( not self.checkIfFileExists(artGenerator.pathToOutputData) ):
                    pass;

                self.generationQueue_.append(artGenerator);
                self.logger.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.processGenerationQueue: File Found and Added to Output Queue");

# Need to determine if current exit strategy is OK, or if we want a more SW heavy approach using personally declared files.
#   This does not need to be OOP. Could use helper functions to determine if too much data in folder, program is stopped recording,
#   etc before closing out the program .
# Is there a way to add paths for TD either in TD or by some helper function that is called to add to sys path prior to each individula
#   function requiring AGD code?
# Is there a way to automate / load in personal files without having to hardcode in the directory? Can an expression be used using the ROOT_DIR, etc
#   to dynamically select where the file is so the program can be console independent? Can all of this happen at runtime?

# We should probably update our documentation for code style and create documentation for naming policies to adhere to in Touch Designer so the Py Developers
#   and TD Designers are on the same page regarding their implementations. 
# Standardize everything. 


# It seems that once we open touch designer, it will block all other processing. It may be good to throw this in its own thread that handles the generation. This removes the need to handle any
#  signals sent back to teh system since we know that if td closes, it has finished processing and if it finishes processing, that we can dequeue the current object, and start processing on the next object

# Think through what can be edited / what should be static. What is really the best way to implement this. 

# May need to create a virtual environemnt relative to the project path that can be used so Touch Designer can work on any machine.
#  Currently I am hardcoding values for my laptop in terms of python libraries, python files, etc. 
# Use this for importing modules: https://nvoid.gitbooks.io/introduction-to-touchdesigner/content/Python/9-6-External-Modules.html