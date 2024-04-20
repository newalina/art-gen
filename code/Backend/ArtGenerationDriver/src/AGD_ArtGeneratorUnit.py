
# Public Modules
from subprocess import run
import sys;
import td;
import json

# Project Modules
from AGD_TouchDesignerPatch import AGD_TouchDesignerPatch as AGD_TDP
from AGD_Definitions import AGD_Directories as AGD_DIR

# Maybe separate into other modules (JSON Specific, TD Specific). These can then be applied as class members
#  within this class? 
class AGD_ArtGeneratorUnit:

    instance_id_ = 0;

    def __init__(self, *args):

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
                print("ERROR: Unable to properly initialize object " + str(self.instance_id_) + "\n");

            self.instance_id_ = AGD_ArtGeneratorUnit.instance_id_;
            AGD_ArtGeneratorUnit.instance_id_ = AGD_ArtGeneratorUnit.instance_id_ + 1;

            print("Created Object: " + str(self.instance_id_));
        elif(len(args) == 0):
            self.readFromJSON();
            print("Initialized with JSON Data for ID: " + str(self.instance_id_));

        else:
            print("ERROR: Invalid Attempt to Initialize Art Generator Object")


    def startTouchDesigner(self):
        executeString = AGD_DIR.TD_EXEC + " " + self.pathToPatch;
        
        # Before Running, we need to pull in all data here that will be used to manipulate
        self.updateArtGenerationData();

        errCode = run(executeString);

        if(errCode.returncode != 0):
            print("ERROR: Unable to run Touch Designer with exit code: " + str(errCode.returncode));
        
    
    def updateArtGenerationData(self):
        return None;

    def packageJSONData(self):

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
            print("WARNING: NONE Mode is only activated for debug and development purposes");
            jsonData["NONE"] = "True";
        else:
            print("ERROR: Unsupported Data to Package\n");
            return -1;

        return jsonData;

    def writeToJSON(self):

        jsonData = self.packageJSONData();

        print(AGD_DIR.AGD_INPUT_JSON);
        with open(str(AGD_DIR.AGD_INPUT_JSON) , "w") as jsonFile:
            json.dump(jsonData, jsonFile);
        
        return 0;
    




