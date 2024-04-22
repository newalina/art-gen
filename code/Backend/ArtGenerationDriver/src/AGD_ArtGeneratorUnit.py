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
import sys;
import json
# TODO: Remove this and generalize path loading
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/Common/src/')

# Project Modules
from AGD_TouchDesignerPatch import AGD_TouchDesignerPatch as AGD_TDP
from AGD_Definitions import AGD_Directories as AGD_DIR
from CMN_ErrorLogging import CMN_LoggingLevels as CMN_LL
from CMN_ErrorLogging import log

# Class Definitions
class AGD_ArtGeneratorUnit:

    instance_id_ = 0;

    #####################################################################
    # Function:     __init__
    # Purpose:      Initialize a new instance of the AGD_ArtGeneratorUnit
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member
    #               args - An optional input that determines if the class
    #                is initialzied from a dataset or JSON file.         
    # Outputs:      None  
    #####################################################################
    def __init__(self, *args):

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: In")

        if(len(args) == 4):

            self.artDriverID = args[0];
            self.paramX = args[1];
            self.paramY = args[2];
            self.paramZ = args[3];

            self.pathToPatch = AGD_TDP.getPathToPatch(self.artDriverID);
            self.pathToOutputData = AGD_DIR.AGD_DATA_DIR + AGD_DIR.AGD_OUTPUT_FILE_BASE + str(self.instance_id_) + '.mov'; # Can make more robust file extensions.
            # Store required parameters for generation here?


            # Store Art Generation Output Here?
            self.generatedOutput = 0;

            if(self.pathToPatch == -1):
                log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__: Unable to properly initialize object " + str(self.instance_id_));

            self.instance_id_ = AGD_ArtGeneratorUnit.instance_id_;
            AGD_ArtGeneratorUnit.instance_id_ = AGD_ArtGeneratorUnit.instance_id_ + 1;

            log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: Created object " + str(self.instance_id_));

        elif(len(args) == 0):
            self.readFromJSON();
            log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__: Initialized with JSON data for object " + str(self.instance_id_));

        else:
            log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__: Invalid Attempt to Initialize Art Generator Object");

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit: Out")


    #####################################################################
    # Function:     startTouchDesigner
    # Purpose:      Start a Touch Designer instance using the data of this
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def startTouchDesigner(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.startTouchDesigner() in")

        executeString = AGD_DIR.TD_EXEC + " " + self.pathToPatch;
        
        # Before Running, we need to pull in all data here that will be used to manipulate
        self.updateArtGenerationData();

        errCode = run(executeString);

        if(errCode.returncode != 0):
            print("ERROR: Unable to run Touch Designer with exit code: " + str(errCode.returncode));
        
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.startTouchDesigner() out")
    
    #####################################################################
    # Function:     updateArtGenerationData
    # Purpose:      Update class member data from external API JSON Files
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def updateArtGenerationData(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.updateArtGenerationData() in")
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.updateArtGenerationData() out")
        return None;

    #####################################################################
    # Function:     packageJSONData
    # Purpose:      Create a JSON object that is used to store the 
    #                parameters of this class. This is the data that is
    #                accessed in Touch Designer. 
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      jsonData - A JSON Object containing the required
    #                data for Touch Designer processing.   
    #####################################################################
    def packageJSONData(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.packagaeJSONData() in")
        jsonData = {};

        # Add Shared Data
        jsonData["eventID"] = self.instance_id_;
        jsonData["moduleID"] = self.artDriverID;
        jsonData["ParamX"] = self.paramX;
        jsonData["ParamY"] = self.paramY;
        jsonData["ParamZ"] = self.paramZ;
        jsonData["OutputPath"] = self.pathToOutputData;

        # Add Driver Specific Data
        if(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_1.value):
            jsonData["SEA"] = "SAW";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_2.value):
            jsonData["WOODS"] = "BURN";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_3.value):
            jsonData["ICE"] = "T";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_4.value):
            jsonData["TRASH"] = "CAN";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_5.value):
            jsonData["RES"] = "5";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_6.value):
            jsonData["RES"] = "6";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_7.value):
            jsonData["RES"] = "7";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_RESERVED_8.value):
            jsonData["RES"] = "8";

        elif(self.artDriverID == AGD_TDP.TD_PATCH_NONE.value):
            log.log(CMN_LL.ERR_LEVEL_WARNING, "AGD_ArtGeneratorUnit.packagaeJSONData() NONE Mode is for debug and development purposes")
            jsonData["NONE"] = "True";
        else:
            log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.packagaeJSONData() Unsupported Data to Package")
            return -1;

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.packagaeJSONData() out")
        return jsonData;

    #####################################################################
    # Function:     writeToJSON
    # Purpose:      Write a JSON object to file
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None
    #####################################################################
    def writeToJSON(self):
        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.writeToJSON() in")
        jsonData = self.packageJSONData();

        with open(str(AGD_DIR.AGD_INPUT_JSON) , "w") as jsonFile:
            json.dump(jsonData, jsonFile);

        log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.writeToJSON() out")
        return 0;
    




