# Public Modules
import git
import os
from enum import Enum, IntEnum, StrEnum
from shutil import which


# Project Modules

def getProjectRoot(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = str(git_repo.git.rev_parse("--show-toplevel"))

    # Do some manipulation of string to make it windows compatible
    return git_root.replace('/', '\\');


# Only works if TD is on the PATH of machine executing this command. Hopefully there is a better
#  way to do this
def getTouchDesignerExecutable():
    try:
        # Do some manipulation of string to cover any potential issues of
        #  spaces in path.
        return '"' + str(which("TouchDesigner")) + '"';
    except:
        print("ERROR: Failed to Find Touch Designer Executable. Is it on your PATH?");
        return None;

# It is probably best to separate enums into different classes depending on what their respective
#  type is, similar to a C / C++ enum would be by type. For initial implementation, this is OK. 
class AGD_Definitions(Enum):
    MAX_QUEUE_SIZE = 64;


class AGD_Directories(StrEnum):
    ROOT_DIR = getProjectRoot(os.getcwd());
    TD_DIR = '\\code\\TouchDesigner';
    TD_EXEC = getTouchDesignerExecutable();
    AGD_DATA_DIR = ROOT_DIR + '\\code\\Backend\\ArtGenerationDriver\\data';
    AGD_INPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataInput.json';
    AGD_OUTPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataOutput.json';
    AGD_OUTPUT_FILE_BASE = '\\artGenerationOutput_';
    AGD_LOGGING_PATH_BASE = ROOT_DIR + '\\code\\Backend\\Common\\logs'

class AGD_RecordingParameters(IntEnum):
    AGD_RECORDING_OFF = 0;
    AGD_RECORDING_ON = 1;
    AGD_RECORDING_DURATION = 5; # In seconds

class AGD_TouchDesignerNodes(StrEnum):
    AGD_TD_RECORD_NODE = 'AGD_RecordOutput';
    AGD_TD_TIMER_NODE  = 'AGD_Timer';
    AGD_TD_TIMER_CALLBACK_NODE = 'AGD_TimerCallbacks'
    AGD_TD_TIMER_TRIGGER = 'AGD_StartTrigger';  
    AGD_TD_PATCH_CONTROL = 'AGD_LaunchGeneration';
    AGD_TD_PATCH_CONTROL_EXEC = 'AGD_LaunchGeneration_exec'

class AGD_LengthUnits(IntEnum):
    LENGTH_UNIT_SAMPLES = 0
    LENGTH_UNIT_FRAMES  = 1
    LENGTH_UNIT_SECONDS = 2

