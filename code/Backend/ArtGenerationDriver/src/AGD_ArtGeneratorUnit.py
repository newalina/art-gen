##########################################################################
#
# File: AGD_ArtGeneratorUnit.py
# 
# Purpose of File: The purpose of this file is to contain the class that
#                   contains the data passed to the Art Generation Driver
#                   from the Backend Command Interface. This class is what
#                   is used to start a touch designer instance.
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
from subprocess import run
import json

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_UnitInitializationTypes as AGD_UIT
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
# from Backend.BackEndCommandInterface.flask.app import logging as log

# Class Definitions
class AGD_ArtGeneratorUnit:

    instance_id_ = 0;

    #####################################################################
    # Method:       __init__
    # Purpose:      Initialize a new instance of the AGD_ArtGeneratorUnit
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member
    #               args - An optional input that determines if the class
    #                is initialzied from a dataset or JSON file.         
    # Outputs:      None  
    #####################################################################
    def __init__(self, *args):

        # log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: In")

        if(len(args) == AGD_UIT.AGD_UIT_DATA):

            self.instance_id_ = AGD_ArtGeneratorUnit.instance_id_;
            AGD_ArtGeneratorUnit.instance_id_ = AGD_ArtGeneratorUnit.instance_id_ + 1;

            self.artDriverID_ = args[0];
            self.paramX_ = args[1];
            self.paramY_ = args[2];
            self.paramZ_ = args[3];
            self.logger_ = args[4];

            self.pathToPatch_ = AGD_TDP.getPathToPatch(self.artDriverID_);
            self.pathToOutputData_ = AGD_DIR.AGD_OUTPUT_FILE_BASE + str(self.instance_id_) + '.mov'; # Can make more robust file extensions.
            # Store required parameters for generation here?


            # Store Art Generation Output Here?
            self.generatedOutput_ = 0;

            if(self.pathToPatch_ == -1):
                self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__: Unable to properly initialize object " + str(self.instance_id_));

            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: Created object " + str(self.instance_id_));

        elif(len(args) == AGD_UIT.AGD_UIT_JSON):
            self.logger_ = args[1];
            self.readFromJSON();
            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: Initialized with JSON data for object " + str(self.instance_id_));
        else:
            self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__: Invalid Attempt to Initialize Art Generator Object");

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit: Out")


    #####################################################################
    # Method:       startTouchDesigner
    # Purpose:      Start a Touch Designer instance using the data of this
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def startTouchDesigner(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.startTouchDesigner() in")

        executeString = str(CMN_DIR.TD_EXEC) + " " + self.pathToPatch_;
        
        # Before Running, we need to pull in all data here that will be used to manipulate
        self.updateArtGenerationData();

        errCode = run(executeString);

        if(errCode.returncode != 0):
            print("ERROR: Unable to run Touch Designer with exit code: " + str(errCode.returncode));
        
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.startTouchDesigner() out")
    
    #####################################################################
    # Method:       updateArtGenerationData
    # Purpose:      Update class member data from external API JSON Files
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def updateArtGenerationData(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.updateArtGenerationData() in")
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.updateArtGenerationData() out")
        return None;

    #####################################################################
    # Method:       packageJSONData
    # Purpose:      Create a JSON object that is used to store the 
    #                parameters of this class. This is the data that is
    #                accessed in Touch Designer. 
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      jsonData - A JSON Object containing the required
    #                data for Touch Designer processing.   
    #####################################################################
    def packageJSONData(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.packagaeJSONData() in")
        jsonData = {};

        # Add Shared Data
        jsonData["eventID"] = self.instance_id_;
        jsonData["moduleID"] = self.artDriverID_;
        jsonData["ParamX"] = self.paramX_;
        jsonData["ParamY"] = self.paramY_;
        jsonData["ParamZ"] = self.paramZ_;
        jsonData["OutputPath"] = self.pathToOutputData_;

        # Add Driver Specific Data
        if(self.artDriverID_ == AGD_TDP.TD_PATCH_LOOP.value):
            jsonData["SEA"] = "SAW";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_SHORE.value):
            jsonData["WOODS"] = "BURN";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_INSTANCE.value):
            jsonData["ICE"] = "T";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_PARTICLE.value):
            jsonData["TRASH"] = "CAN";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_WATERCOLOR.value):
            jsonData["RES"] = "5";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_RESERVED_6.value):
            jsonData["RES"] = "6";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_RESERVED_7.value):
            jsonData["RES"] = "7";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_RESERVED_8.value):
            jsonData["RES"] = "8";

        elif(self.artDriverID_ == AGD_TDP.TD_PATCH_NONE.value):
            self.logger_.log(CMN_LL.ERR_LEVEL_WARNING, "AGD_ArtGeneratorUnit.packagaeJSONData() NONE Mode is for debug and development purposes")
            jsonData["NONE"] = "True";
        else:
            self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.packagaeJSONData() Unsupported Data to Package")
            return -1;

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.packagaeJSONData() out")
        return jsonData;

    #####################################################################
    # Method:       writeToJSON
    # Purpose:      Write a JSON object to file
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None
    #####################################################################
    def writeToJSON(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.writeToJSON() in")
        jsonData = self.packageJSONData();

        with open(str(AGD_DIR.AGD_INPUT_JSON) , "w") as jsonFile:
            json.dump(jsonData, jsonFile);

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.writeToJSON() out")
        return 0;