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

# Public Modules
import json
import sys
import td

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_LengthUnits as AGD_LU
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_RecordingParameters as AGD_RP
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TimerState as AGD_TS
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_VideoCodecTypes as AGD_VCT
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_ErrorCodes as CMN_EC

# Class Definitions
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
        # Create class members
        self.instance_id_ = -1;
        self.artDriverID_ = -1;
        self.paramA_ = -1;
        self.paramB_ = -1;
        self.paramC_ = -1;
        self.paramD_ = -1;
        self.paramE_ = -1;
        self.paramF_ = -1;
        self.pathToOutputData_ = -1;
    
        # Initialize class members from JSON
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
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.run() in")

        # Initialize TD Patch. If invalid, quit out of Touch Designer
        if(self.initializeTouchDesigner() != CMN_EC.CMN_ERR_OK):
            #log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_TouchDesignerInstance.run() Unable to initialize Touch Designer")
            quit();
        
        # Start Art Generation
        self.startArtGeneration();
    
        # Start Exit Delay
        self.startGenerationDelay();
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.run() out")

    #####################################################################
    # Method:       initializeTouchDesigner
    # Purpose:      Set the parameters for required Touch Designer 
    #                objects for correct processing. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      err - An error code of how the processing completed
    #####################################################################
    def initializeTouchDesigner(self):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializeTouchDesigner() in");
        err = CMN_EC.CMN_ERR_OK;

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
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = AGD_TS.AGD_TIMER_OFF;

        # Initialize Specific Patch Parameters
        err = self.initializePatch();

        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializeTouchDesigner() out")
        return err;

    #####################################################################
    # Method:       initializePatch
    # Purpose:      Set the parameters for the artisitc parameters that
    #                an individual art generation module uses.  
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      err - An error code of how processing completed  
    #####################################################################
    def initializePatch(self):
         #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializePatch() in")

        if(self.artDriverID_ == AGD_TDP.TD_PATCH_NONE):
            return CMN_EC.CMN_ERR_OK;
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
            #log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_TouchDesignerInstance.initializePatch() Invalid Touch Designer Module")
            return CMN_EC.CMN_ERR_INVALID_DATA;

         #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.initializePatch() out")
        return CMN_EC.CMN_ERR_OK;

    #####################################################################
    # Method:       hextoRGB
    # Purpose:      A helper method that computes RGB values from an
    #                input hexademical number. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      red - FP value of red from 0 to 1.0
    #               green - FP value of green from 0 to 1.0
    #               blue - FP value of blue from 0 to 1.0
    #####################################################################
    def hextoRGB(self, hexIn):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.hextoRGB() in")

        red = ((hexIn >> 16) & 0xff) / 0xff;
        green = ((hexIn >> 8) & 0xff) / 0xff;
        blue = (hexIn & 0xff) / 0xff;

        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.hextoRGB() out")
        return red, green, blue;

    #####################################################################
    # Method:       startArtGeneration
    # Purpose:      Enable recording for art generation
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startArtGeneration(self):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.startArtGeneration() in")

        # Enable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_ON.value;

        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.startArtGeneration() out")

    #####################################################################
    # Method:       startGenerationDelay
    # Purpose:      Start a fixed-time delay that is used to close Touch
    #                Designer after generation is complete. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def startGenerationDelay(self):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.startGenerationDelay() in")
            
        # Start the timer
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = AGD_TS.AGD_TIMER_ON;
        
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.startGenerationDelay() out")
    
    #####################################################################
    # Method:       stopArtGeneration
    # Purpose:      Stop art generation after a fixed amount of time.
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def stopArtGeneration(self):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.stopArtGeneration() in")

        # Disable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_OFF.value;

        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.stopArtGeneration() out")

    #####################################################################
    # Method:       readFromJSON
    # Purpose:      Read in data from JSON file to populate the class. 
    # Requirements: N/A
    # Inputs:       self - current class member        
    # Outputs:      None  
    #####################################################################
    def readFromJSON(self):
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.readFromJSON() in")
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
                #log.log(CMN_LL.ERR_LEVEL_WARNING, f"AGD_TouchDesignerInstance.readFromJSON() input key ({key})is not supported")
                continue;
        
        #log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_TouchDesignerInstance.readFromJSON() out")