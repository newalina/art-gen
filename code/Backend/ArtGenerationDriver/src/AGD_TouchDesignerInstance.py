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
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_LengthUnits as AGD_LU
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_RecordingParameters as AGD_RP
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_VideoCodecTypes as AGD_VCT
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL


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
    # Method:       __init__
    # Purpose:      Initialize a new instance of the 
    #                AGD_TouchDesignerInstance class
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def __init__(self):
        # Give garabge data
        self.instance_id_ = -1;
        self.artDriverID_ = -1;
        self.paramA_ = -1;
        self.paramB_ = -1;
        self.paramC_ = -1;
        self.paramD_ = -1;
        self.paramE_ = -1;
        self.paramF_ = -1;
        self.pathToOutputData_ = -1;
    
        self.readFromJSON();
    
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.__init__: Init complete")

    #####################################################################
    # Method:       run
    # Purpose:      Run Touch Designer using the data from the current
    #                class object.
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def run(self):
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.run: beginning run")
        self.initializeTouchDesigner();

        self.startArtGeneration();
    
        # Right now a delay goes through a timer object, which can then be used to call a callback to exit out of TD.
        #  Ideally it would be nice to use a class method to handle the stopping of recording cleanly, and then exiting.
        #  THe current implementation works for now.

        sys.stdout.write("Starting Delay");
        self.startGenerationDelay();
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.run: run complete")

    #####################################################################
    # Method:       initializeTouchDesigner
    # Purpose:      Set the parameters for required Touch Designer 
    #                objects for correct processing. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def initializeTouchDesigner(self):
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.initializeTouchDesigner: initializing Touch Designer")
        # Initialize Recording Node

        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_OFF.value;
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.videocodec = AGD_VCT.AGD_CODEC_PHOTO_MOTION_JPEG;
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.file = self.pathToOutputData_;
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.limitlength = 1; # Create def for this
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.length = AGD_RP.AGD_RECORDING_DURATION;
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.lengthunit = AGD_LU.LENGTH_UNIT_SECONDS;

        # Initialize Timer Node
        td.op(AGD_TDN.AGD_TD_TIMER_NODE).par.length = AGD_RP.AGD_RECORDING_DURATION + AGD_RP.AGD_RECORDING_DELAY;
        td.op(AGD_TDN.AGD_TD_TIMER_NODE).par.lengthunits = AGD_LU.LENGTH_UNIT_SECONDS;
        
        # Initialize Timer Trigger
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = 0;

        # Initialize Specific Patch
        self.initializePatch();

        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.initializeTouchDesigner: Touch Designer initialized")
        return 0;


    def initializePatch(self):
         #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializePatch() in")

        if(self.artDriverID_ == AGD_TDP.TD_PATCH_NONE):
            return
        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_LOOP):
            td.op("grid1").par.sizex = self.paramA_;
            td.op("grid1").par.sizey = self.paramB_;
            td.op("math3").par.gain = self.paramC_;
            td.op("feedback/level1").par.gamma1 = self.paramD_;

            red, green, blue = self.hextoRGB(self.paramE_);
            td.op("constant1").par.colorr = red;
            td.op("constant1").par.colorg = green;
            td.op("constant1").par.colorb = blue;


        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_SHORE):
            td.op("noise1").par.amp = self.paramA_;
            td.op("noise1").par.harmon = self.paramB_;
            td.op("cam1").par.tz = self.paramC_;

            red, green, blue = self.hextoRGB(self.paramD_);
            td.op("line1").par.linenearcolorr = red;
            td.op("line1").par.linenearcolorg = green;
            td.op("line1").par.linenearcolorb = blue;
        
        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_INSTANCE):
            td.op("noise1").par.rate = self.paramA_;
            td.op("noise1").par.amp = self.paramB_;
            td.op("noise1").par.period = self.paramC_;
            td.op("noise1").par.periodunit = AGD_LU.LENGTH_UNIT_SECONDS;
            
            td.op("moviefilein1").par.file = AGD_DIR.AGD_TD_IMG_SRC_DIR + 'nasa-image-otd.jpg';

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_HEX_QUAKE):
            td.op("noise4").par.amp = self.paramA_;
            td.op("noise4").par.period = self.paramB_;
            td.op("noise4").par.gain = self.paramC_;

            red, green, blue = self.hextoRGB(self.paramD_);
            td.op("ramp5_keys")[1,1].val = red;
            td.op("ramp5_keys")[1,2].val = green;
            td.op("ramp5_keys")[1,3].val = blue;

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_WATERCOLOR):
            td.op("displace1").par.displaceweightx = self.paramA_;
            td.op("displace1").par.displaceweighty = self.paramB_;
            td.op("displace1").par.uvweight = self.paramC_;
            td.op("emboss1").par.strength = self.paramD_;

            td.op("moviefilein1").par.file = AGD_DIR.AGD_TD_IMG_SRC_DIR + 'nasa-image-otd.jpg';

        else:
            #log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_TouchDesignerInstance.initializePatch: Invalid Touch Designer Module")
            return

         #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializePatch() out")
        return



    def hextoRGB(self, hexIn):

        red = ((hexIn >> 16) & 0xff) / 0xff;
        green = ((hexIn >> 8) & 0xff) / 0xff;
        blue = (hexIn & 0xff) / 0xff;

        return red, green, blue;


    #####################################################################
    # Method:       startArtGeneration
    # Purpose:      Enable recording for art generation
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startArtGeneration(self):
        # Enable output recording
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.startArtGeneration: starting art generation")
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_ON.value;
        return 0;

    #####################################################################
    # Method:       startGenerationDelay
    # Purpose:      Start a fixed-time delay that is used to close Touch
    #                Designer after generation is complete. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startGenerationDelay(self):
        # Start the timer
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = 1;
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.startGenerationDelay: starting generation after delay")
    
    #####################################################################
    # Method:       stopArtGeneration
    # Purpose:      Stop art generation after a fixed amount of time.
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def stopArtGeneration(self):
        # Disable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_OFF.value;
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.stopArtGeneration: stopping art generation")
        return 0;

    #####################################################################
    # Method:       readFromJSON
    # Purpose:      Read in data from JSON file to populate the class. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def readFromJSON(self):
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.readFromJSON: reading in data from JSON")
        with open(str(AGD_DIR.AGD_INPUT_JSON), "r") as jsonFile:
            jsonData = json.load(jsonFile);

        for key in jsonData.keys():
            if(key == "eventID"):
                self.instance_id_ = jsonData[key];
            elif(key == "moduleID"):
                self.artDriverID_ = jsonData[key];
            elif(key == "ParamA"):
                self.paramA_ = jsonData[key];
            elif(key == "ParamB"):
                self.paramB_ = jsonData[key];
            elif(key == "ParamC"):
                self.paramC_ = jsonData[key];
            elif(key == "ParamD"):
                self.paramD_ = jsonData[key];
            elif(key == "ParamE"):
                self.paramE_ = jsonData[key];
            elif(key == "ParamF"):
                self.paramF_ = jsonData[key];
            elif(key == "OutputPath"):
                self.pathToOutputData_ = jsonData[key];
            else:
                print("WARNING: " + str(key) + " is not supported");
        
        #log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_TouchDesignerInstance.readFromJSON: read in data from JSON")
        return 0;