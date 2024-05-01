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
import threading
from collections import deque
import os

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Definitions as AGD_DEF;
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL

# Class Definitions
class AGD_Subsystem:

    #####################################################################
    # Method:       __init__
    # Purpose:      Initialize a new instance of the AGD_Subsystem class
    # Requirements: N/A
    # Inputs:       self - current class member
    #               logger - An object containing the logging class
    #                that is used for recording the execution of the
    #                software.      
    # Outputs:      None  
    #####################################################################
    def __init__(self, logger):
        self.logger_ = logger;
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.__init__() in");

        # Initialize class
        self.generationQueue_ = deque();
        self.generatedOutput_ = deque();
        self.generationThread_ = None;
        self.startProcess();

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.__init__() out");
    
    #####################################################################
    # Method:       startProcess
    # Purpose:      Initialize and start a thread to handle the art
    #                generation queue.
    # Requirements: N/A
    # Inputs:       self - current class member     
    # Outputs:      None
    #####################################################################
    def startProcess(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.startProcess() in");

        # init a thread to handle the generation queue
        self.generationThread_ = threading.Thread(target=self.processGenerationQueue);
        self.generationThread_.start();

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.startProcess() out");

    #####################################################################
    # Method:       appendGenerationRequest
    # Purpose:      Add an AGD_ArtGeneratorUnit object to the queue for
    #                processing in Touch Designer
    # Requirements: N/A
    # Inputs:       self - current class member     
    #               object - The AGD_ArtGeneratorUnit to be appended for
    #                art generation.  
    # Outputs:      None
    #####################################################################
    def appendGenerationRequest(self, object) -> int:
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.appendGenerationRequest() in");

        if( len(self.generationQueue_) >= AGD_DEF.MAX_QUEUE_SIZE.value ):
            self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_Subsystem.appendGenerationRequest() Cannot add request to queue. Queue is full.");
            return -1;
        else:
            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.appendGenerationRequest() Appending Generation Request");
            self.generationQueue_.append(object);

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.appendGenerationRequest() out");   
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
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.popGenerationRequest() Popping Generation Request");
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
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.checkIfFileExists() Checking if File Exists");
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
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Subsystem.processGenerationQueue() in");        
        while(True):
            if( len(self.generationQueue_) > 0 ):
                self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.processGenerationQueue() processing new unit"); 
                moduleID, paramA, paramB, paramC, paramD, paramE, paramF = self.popGenerationRequest();
                artGenerator = AGD_ArtGeneratorUnit(moduleID, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
                artGenerator.writeToJSON();
                artGenerator.startTouchDesigner();

                # check if the file exists
                while( not self.checkIfFileExists(artGenerator.pathToOutputData_) ):
                    pass;

                self.generatedOutput_.append(artGenerator);
                self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Subsystem.processGenerationQueue() File Found and Added to Output Queue");