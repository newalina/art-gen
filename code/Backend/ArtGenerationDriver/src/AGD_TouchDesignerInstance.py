import json
import sys
import td

from AGD_Definitions import AGD_LengthUnits as AGD_LU
from AGD_Definitions import AGD_RecordingParameters as AGD_RP
from AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN
from AGD_Definitions import AGD_Directories as AGD_DIR

class AGD_TouchDesignerInstance:

    def __init__(self):
        # Give garabge data
        self.instance_id_ = -1;
        self.artDriverID = -1;
        self.paramX = -1;
        self.paramY = -1;
        self.paramZ = -1;
        self.pathToOutputData = -1;
    
        self.readFromJSON();


    def run(self):

        self.initializeTouchDesigner();

        self.startArtGeneration();
    
        # Right now a delay goes through a timer object, which can then be used to call a callback to exit out of TD.
        #  Ideally it would be nice to use a class method to handle the stopping of recording cleanly, and then exiting.
        #  THe current implementation works for now.
        self.startGenerationDelay();


    def initializeTouchDesigner(self):

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

        return 0;


    def startArtGeneration(self):
        # Enable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_ON.value;
        return 0;

    def startGenerationDelay(self):
        # Start the timer
        td.op(AGD_TDN.AGD_TD_TIMER_TRIGGER).par.const0value = 1;
    
    def stopArtGeneration(self):
        # Disable output recording
        td.op(AGD_TDN.AGD_TD_RECORD_NODE).par.record = AGD_RP.AGD_RECORDING_OFF.value;
        return 0;

    def readFromJSON(self):

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
        return 0;