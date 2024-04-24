##########################################################################
#
# File: AGD_TouchDesignerInstance.py
# 
# Purpose of File: The purpose of this file is to contain the class used
#                   by Touch Designer to perform all processing for art
#                   generation. 
#
# Creation Date: April 14th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Includes
import json
import sys
import td

# Private Includes
from AGD_Definitions import AGD_LengthUnits as AGD_LU
from AGD_Definitions import AGD_RecordingParameters as AGD_RP
from AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN
from AGD_Definitions import AGD_Directories as AGD_DIR

from Backend.BackEndCommandInterface.flask.app import logging as log
from Backend.Common.src.CMN_ErrorLogging import CMN_LoggingLevels as CMN_LL


##########################################################################
#
# Class: AGD_TouchDesignerInstance
#
# Purpose: The purpose of this class is to contain the Touch Designer
#           instance that is used to generate art.
#
##########################################################################
class AGD_TouchDesignerInstance:

    #####################################################################
    # Function:     __init__
    # Purpose:      Initialize a new instance of the 
    #                AGD_TouchDesignerInstance class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self):
        # Give garabge data
        self.instance_id_ = -1;
        self.artDriverID = -1;
        self.paramX = -1;
        self.paramY = -1;
        self.paramZ = -1;
        self.pathToOutputData = -1;
    
        self.readFromJSON();
    
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.__init__: Init complete")

    #####################################################################
    # Function:     run
    # Purpose:      Run Touch Designer using the data from the current
    #                class object.
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def run(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.run: beginning run")
        self.initializeTouchDesigner();

        self.startArtGeneration();
    
        # Right now a delay goes through a timer object, which can then be used to call a callback to exit out of TD.
        #  Ideally it would be nice to use a class method to handle the stopping of recording cleanly, and then exiting.
        #  THe current implementation works for now.
        self.startGenerationDelay();
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.run: run complete")

    #####################################################################
    # Function:     initializeTouchDesigner
    # Purpose:      Set the parameters for required Touch Designer 
    #                objects for correct processing. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def initializeTouchDesigner(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.initializeTouchDesigner: initializing Touch Designer")
        # Initialize Recording Node
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.file = self.pathToOutputData;
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.limitlength = 1; # Create def for this
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.length = AGD_RP.AGD_RECORDING_DURATION; # Create def for this
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.lengthunit = AGD_LU.LENGTH_UNIT_SECONDS; # Create def for this (0 -> index, 1 -> frames, 2 -> seconds)

        # Initialize Timer Node
        td.op(AGD_TDN.AGD_TD_TIMER_NODE).par.length = AGD_RP.AGD_RECORDING_DURATION;
        td.op(AGD_TDN.AGD_TD_TIMER_NODE).par.lengthunits = AGD_LU.LENGTH_UNIT_SECONDS;
        
        # Initialize Timer Trigger
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = 0;

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.initializeTouchDesigner: Touch Designer initialized")
        return 0;

    #####################################################################
    # Function:     startArtGeneration
    # Purpose:      Enable recording for art generation
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startArtGeneration(self):
        # Enable output recording
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.startArtGeneration: starting art generation")
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_ON.value;
        return 0;

    #####################################################################
    # Function:     startGenerationDelay
    # Purpose:      Start a fixed-time delay that is used to close Touch
    #                Designer after generation is complete. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startGenerationDelay(self):
        # Start the timer
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = 1;
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.startGenerationDelay: starting generation after delay")
    
    #####################################################################
    # Function:     stopArtGeneration
    # Purpose:      Stop art generation after a fixed amount of time.
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def stopArtGeneration(self):
        # Disable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_OFF.value;
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.stopArtGeneration: stopping art generation")
        return 0;

    #####################################################################
    # Function:     readFromJSON
    # Purpose:      Read in data from JSON file to populate the class. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def readFromJSON(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.readFromJSON: reading in data from JSON")
        with open(str(AGD_DIR.AGD_INPUT_JSON), "r") as jsonFile:
            jsonData = json.load(jsonFile);

        for key in jsonData.keys():
            if(key == "eventID"):
                self.instance_id_ = jsonData[key];
            elif(key == "moduleID"):
                self.artDriverID = jsonData[key];
            elif(key == "ParamX"):
                self.paramX = jsonData[key];
            elif(key == "ParamY"):
                self.paramY = jsonData[key];
            elif(key == "ParamZ"):
                self.paramZ = jsonData[key];
            elif(key == "OutputPath"):
                self.pathToOutputData = jsonData[key];
            else:
                print("WARNING: " + str(key) + " is not supported");
        
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.readFromJSON: read in data from JSON")
        return 0;