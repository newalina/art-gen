# Public Modules
import git
import os
from enum import Enum, IntEnum
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
    ROOT_DIR = getProjectRoot(os.getcwd());
    TD_DIR = '\\code\\TouchDesigner';
    TD_EXEC = getTouchDesignerExecutable();
    AGD_DATA_DIR = ROOT_DIR + '\\code\\Backend\\ArtGenerationDriver\\data';
    AGD_INPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataInput.json';
    AGD_OUTPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataOutput.json';
    AGD_OUTPUT_FILE_BASE = '\\artGenerationOutput_';

    MAX_QUEUE_SIZE = 64;
    AGD_RECORDING_OFF = 0;
    AGD_RECORDING_ON = 1;

    AGD_TD_RECORD_NODE = 'agd_recordOutput';
    AGD_TD_TIMER_NODE  = 'agd_timer';
    AGD_TD_TIMER_TRIGGER = 'agd_startTrigger';


class AGD_LengthUnits(IntEnum):
    LENGTH_UNIT_SAMPLES = 0
    LENGTH_UNIT_FRAMES  = 1
    LENGTH_UNIT_SECONDS = 2

