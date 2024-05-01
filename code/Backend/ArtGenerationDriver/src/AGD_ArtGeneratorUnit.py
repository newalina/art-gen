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
from json import dump

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Directories as AGD_DIR
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_UnitInitializationTypes as AGD_UIT
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.ArtGenerationDriver.src.AGD_Definitions import TD_PATCH_FILES
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL

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
            self.paramA_ = args[1];
            self.paramB_ = args[2];
            self.paramC_ = args[3];
            self.paramD_ = args[4];
            self.paramE_ = args[5];
            self.paramF_ = args[6];
            self.logger_ = args[7];

            self.pathToPatch_ = TD_PATCH_FILES[self.artDriverID_];
            self.pathToOutputData_ = AGD_DIR.AGD_OUTPUT_FILE_BASE + str(self.instance_id_) + '.mov'; # Can make more robust file extensions.

            # Store Art Generation Output Here?
            self.generatedOutput_ = 0;

            if(self.pathToPatch_ == -1):
                self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__() Unable to properly initialize object " + str(self.instance_id_));

            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__() Created object " + str(self.instance_id_));

        elif(len(args) == AGD_UIT.AGD_UIT_JSON):
            self.logger_ = args[1];
            self.readFromJSON();
            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_ArtGeneratorUnit.__init__() Initialized with JSON data for object " + str(self.instance_id_));
        else:
            #self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.__init__() Invalid Attempt to Initialize Art Generator Object");
            return;
     
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit() Out")


    #####################################################################
    # Method:       startTouchDesigner
    # Purpose:      Start a Touch Designer instance using the data of this
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def startTouchDesigner(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.startTouchDesigner() in")

        executeString = "TouchDesigner " + self.pathToPatch_;
        
        # Before Running, we need to pull in all data here that will be used to manipulate
        self.updateArtGenerationData();

        errCode = run(executeString, shell=True);

        if(errCode.returncode != 0):
            self.logger_.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_ArtGeneratorUnit.startTouchDesigner() Unable to run Touch Designer with exit code: " + str(errCode.returncode))
        
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.startTouchDesigner() out")
    
    #####################################################################
    # Method:       updateArtGenerationData
    # Purpose:      Update class member data from external API JSON Files
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None  
    #####################################################################
    def updateArtGenerationData(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.updateArtGenerationData() in")
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.updateArtGenerationData() out")
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
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.packagaeJSONData() in")
        jsonData = {};

        # Add Shared Data
        jsonData["eventID"] = self.instance_id_;
        jsonData["moduleID"] = self.artDriverID_;
        jsonData["ParamA"] = self.paramA_;
        jsonData["ParamB"] = self.paramB_;
        jsonData["ParamC"] = self.paramC_;
        jsonData["ParamD"] = self.paramD_;
        jsonData["ParamE"] = self.paramE_;
        jsonData["ParamF"] = self.paramF_;
        jsonData["OutputPath"] = self.pathToOutputData_;

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.packagaeJSONData() out")
        return jsonData;

    #####################################################################
    # Method:       writeToJSON
    # Purpose:      Write a JSON object to file
    # Requirements: N/A
    # Inputs:       self - current class member       
    # Outputs:      None
    #####################################################################
    def writeToJSON(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.writeToJSON() in")
        jsonData = self.packageJSONData();

        with open(str(AGD_DIR.AGD_INPUT_JSON) , "w") as jsonFile:
            dump(jsonData, jsonFile);

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_ArtGeneratorUnit.writeToJSON() out")
        return 0;