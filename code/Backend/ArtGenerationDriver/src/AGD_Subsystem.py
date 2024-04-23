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
# Copyright: GPL-3.0-or-later © Copyleft 2024 Alexander Pratt, Alina Kim, David Doan, Erik Wang, Gus LeTourneau, Malique Bodie, Yingjia Liu, Morgann Thain, momothain
#       
##########################################################################

# Public Modules
import logging
import os
import sys
import threading
from collections import deque

# TODO: Remove this and generalize path loading
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/Common/src/')

# Project Modules
from AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from AGD_Definitions import AGD_Definitions as AGD_DEF


# Class Definitions
class AGD_Subsystem:

    #####################################################################
    # Function:     __init__
    # Purpose:      Initialize a new instance of the AGD_Subsystem class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self):
        # expects a list of [modelSelection, param1, param2, param3]
        self.generationQueue = deque()
        self.generatedOutput = deque()

        # init a thread to handle the generation queue
        self.generationThread = threading.Thread(target=self.processGenerationQueue)

    #####################################################################
    # Function:     appendGenerationRequest
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
            print("ERROR: Unable to append to queue")
            return -1
        else:
            self.generationQueue.append(object)
        
        return 0

    #####################################################################
    # Function:     popGenerationRequest
    # Purpose:      Remove an AGD_ArtGeneratorUnit object from the queue 
    #                after it has completed processing
    # Requirements: N/A
    # Inputs:       self - current class member     
    # Outputs:      
    #####################################################################
    def popGenerationRequest(self):
        logging.debug("Popping Generation Request")
        return self.generationQueue.popleft()

    #####################################################################
    # Function:     checkIfFileExists
    # Purpose:      Determine if art generation output file has been
    #                written.
    # Requirements: N/A
    # Inputs:       self - current class member 
    #               path - path to the expected art generation output file    
    # Outputs:      boolean - True if file is found, false if not found  
    #####################################################################
    def checkIfFileExists(self, path):
        return os.path.isfile(path)

    #####################################################################
    # Function:     processGenerationQueue
    # Purpose:      Driving function for the Art Generator Driver that
    #                handles the processing of the request queue. 
    # Requirements: N/A
    # Inputs:       self - current class member  
    # Outputs:      None
    #####################################################################
    def processGenerationQueue(self):
        while(True):
            if( len(self.generationQueue) > 0 ):

                a, param1, param2, param3 = self.popGenerationRequest()
                artGenerator = AGD_ArtGeneratorUnit(a, param1, param2, param3)
                artGenerator.writeToJSON()
                artGenerator.startTouchDesigner()

                # check if the file exists
                while( not self.checkIfFileExists(artGenerator.pathToOutputData) ):
                    pass

                self.generatedOutput.append(artGenerator)                

    


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
