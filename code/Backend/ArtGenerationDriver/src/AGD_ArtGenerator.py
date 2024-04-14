
# Public Modules
from subprocess import run
import sys;
import td;
import json

# Project Modules
from AGD_TouchDesignerPatch import AGD_TouchDesignerPatch as AGD_TDP
from AGD_Definitions import AGD_Definitions as AGD_DEF
from AGD_Definitions import AGD_LengthUnits as AGD_LU

# Maybe separate into other modules (JSON Specific, TD Specific). These can then be applied as class members
#  within this class? 
class AGD_ArtGenerator:

    instance_id_ = 0;

    def __init__(self, *args):

        if(len(args) == 4):

            self.artDriverID = args[0];
            self.paramX = args[1];
            self.paramY = args[2];
            self.paramZ = args[3];

            self.pathToPatch = AGD_TDP.getPathToPatch(self.artDriverID);
            self.pathToOutputData = AGD_DEF.AGD_DATA_DIR.value + AGD_DEF.AGD_OUTPUT_FILE_BASE.value + str(self.instance_id_) + '.mov'; # Can make more robust file extensions.
            # Store required parameters for generation here?


            # Store Art Generation Output Here?
            self.generatedOutput = 0;

            if(self.pathToPatch == -1):
                print("ERROR: Unable to properly initialize object " + str(self.instance_id_) + "\n");

            self.instance_id_ = AGD_ArtGenerator.instance_id_;
            AGD_ArtGenerator.instance_id_ = AGD_ArtGenerator.instance_id_ + 1;

            print("Created Object: " + str(self.instance_id_));
        elif(len(args) == 0):
            self.readFromJSON();
            print("Initialized with JSON Data for ID: " + str(self.instance_id_));

        else:
            print("ERROR: Invalid Attempt to Initialize Art Generator Object")


    def startTouchDesigner(self):
        executeString = AGD_DEF.TD_EXEC.value + " " + self.pathToPatch;
        
        # Before Running, we need to pull in all data here that will be used to manipulate
        self.updateArtGenerationData();

        errCode = run(executeString);

        if(errCode.returncode != 0):
            print("ERROR: Unable to run Touch Designer with exit code: " + str(errCode.returncode));
        
    
    def updateArtGenerationData(self):
        return None;


    def startArtGeneration(self):
        # Update location to store data
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.file = self.pathToOutputData;

        # Set recording time limit
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.limitlength = 1; # Create def for this
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.length = 5; # Create def for this
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.lengthunit = AGD_LU.LENGTH_UNIT_SECONDS; # Create def for this (0 -> index, 1 -> frames, 2 -> seconds)

        # Enable output recording
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.record = AGD_DEF.AGD_RECORDING_ON.value;
        return 0;

    def startGenerationDelay(self):
        # Maybe split this into two different methods (Init Timer, Start Timer)

        # Set timer Parameters limit
        td.op(AGD_DEF.AGD_TD_TIMER_NODE.value).par.length = 5;
        td.op(AGD_DEF.AGD_TD_TIMER_NODE.value).par.lengthunits = AGD_LU.LENGTH_UNIT_SECONDS;

        # Start the timer
        td.op(AGD_DEF.AGD_TD_TIMER_TRIGGER.value).par.const0value = 0;
        td.op(AGD_DEF.AGD_TD_TIMER_TRIGGER.value).par.const0value = 1;
    
    def stopArtGeneration(self):
        # Disable output recording
        sys.stdout.write("Disabling\n");
        td.op(AGD_DEF.AGD_TD_RECORD_NODE.value).par.record = AGD_DEF.AGD_RECORDING_OFF.value;
        return 0;

    
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

        print(AGD_DEF.AGD_INPUT_JSON.value);
        with open(str(AGD_DEF.AGD_INPUT_JSON.value) , "w") as jsonFile:
            json.dump(jsonData, jsonFile);
        
        return 0;
    

    def readFromJSON(self):

        with open(str(AGD_DEF.AGD_INPUT_JSON.value), "r") as jsonFile:
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
        return 0;



