##########################################################################
#
# File: AGD_Definitions.py
# 
# Purpose of File: The purpose of this file is to contain all defined
#                   values that are used in the Art Generator Driver.
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import git
import os
from enum import Enum, IntEnum, StrEnum
from shutil import which


# Project Modules


#####################################################################
# Function:     getProjectRoot
# Purpose:      Find the root of the github repo that this project
#                is being run in. 
# Requirements: N/A
# Inputs:       path - The path to the current working directory.        
# Outputs:      Path to root of GitHub Repository  
#####################################################################
def getProjectRoot(path):
    git_repo = git.Repo(path, search_parent_directories=True)
    git_root = str(git_repo.git.rev_parse("--show-toplevel"))

    # Do some manipulation of string to make it windows compatible
    return git_root.replace('/', '\\');



#####################################################################
# Function:     getTouchDesignerExecutable
# Purpose:      Find the path to the Touch Designer executable on 
#                the current machine. 
# Requirements: N/A
# Inputs:       None      
# Outputs:      Path to the Touch Designer executable
#####################################################################
def getTouchDesignerExecutable():
    # Only works if TD is on the PATH of machine executing this command. Hopefully there is a better
    #  way to do this
    try:
        # Do some manipulation of string to cover any potential issues of
        #  spaces in path.
        return '"' + str(which("TouchDesigner")) + '"';
    except:
        print("ERROR: Failed to Find Touch Designer Executable. Is it on your PATH?");
        return None;


#####################################################################
# Enum:         AGD_Definitions
# Enum Type:    Enum
# Description:  This enum contains general defined values that
#                should be used in the Art Generation Driver.
# Values:
#   MAX_QUEUE_SIZE - Contains the maximum size of the AGD Subsystem
#                       queue. 
#####################################################################
class AGD_Definitions(Enum):
    MAX_QUEUE_SIZE = 64;

#####################################################################
# Enum:         AGD_Directories
# Enum Type:    StrEnum
# Description:  This enum contains strings of directory locations
#                that are used in different capacities in the Art
#                Generation Driver. 
# Values:
#   ROOT_DIR - Contains the root directory of the GitHub Repository
#   TD_DIR - Contains the directory of the Touch Designer relative
#    to ROOT_DIR.
#   TD_EXEC - Contains the directory to the installed Touch Desginer
#    Executable.
#   AGD_DATA_DIR - Contains the path to the Art Generation Driver 
#    data directory
#   AGD_INPUT_JSON - Contains the path to the Art Generation Driver
#    input JSON file
#   AGD_OUTPUT_JSON - Contains the path to the Art Generation Driver
#    output JSON file
#   AGD_OUTPUT_FILE_BASE - Provides a string that is the base of any
#    art generation output file
#   AGD_LOGGING_PATH_BASE - Provides a path to to the error logs
#    directory
#####################################################################
class AGD_Directories(StrEnum):
    ROOT_DIR = getProjectRoot(os.getcwd());
    TD_DIR = '\\code\\TouchDesigner';
    TD_EXEC = getTouchDesignerExecutable();
    AGD_DATA_DIR = ROOT_DIR + '\\code\\Backend\\ArtGenerationDriver\\data';
    AGD_INPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataInput.json';
    AGD_OUTPUT_JSON = AGD_DATA_DIR + '\\artGenerationDataOutput.json';
    AGD_OUTPUT_FILE_BASE = '\\artGenerationOutput_';
    AGD_LOGGING_PATH_BASE = ROOT_DIR + '\\code\\Backend\\Common\\logs'

#####################################################################
# Enum:         AGD_RecordingParameters
# Enum Type:    IntEnum
# Description:  This enum contains integers that are used for
#                adjusting recording parameters in Touch Designer.
# Values:
#   AGD_RECORDING_OFF - Disables recording in Touch Designer
#   AGD_RECORDING_ON - Enables recording in Touch Designer
#   AGD_RECORDING_DURATION - Duration of Touch Designer output (s)
#####################################################################
class AGD_RecordingParameters(IntEnum):
    AGD_RECORDING_OFF = 0;
    AGD_RECORDING_ON = 1;
    AGD_RECORDING_DURATION = 5;

#####################################################################
# Enum:         AGD_TouchDesignerNodes
# Enum Type:    StrEnum
# Description:  This enum contains the standardized names for the
#                various objects needed to control Touch Designer
#                from Python.
# Values:
#   AGD_TD_RECORD_NODE - Node that records art generation output
#   AGD_TD_TIMER_NODE - Node that times and triggers the shutdown
#    of Touch Designer.
#   AGD_TD_TIMER_CALLBACK_NODE - Node that is the callback once the
#    timer has finished its count.
#   AGD_TD_TIMER_TRIGGER - Node that starts the timer count
#   AGD_TD_PATCH_CONTROL - Node that controls the entire patch
#   AGD_TD_PATCH_CONTROL_EXEC - Node that executes the control patch                   
#####################################################################
class AGD_TouchDesignerNodes(StrEnum):
    AGD_TD_RECORD_NODE = 'AGD_RecordOutput';
    AGD_TD_TIMER_NODE  = 'AGD_Timer';
    AGD_TD_TIMER_CALLBACK_NODE = 'AGD_TimerCallbacks'
    AGD_TD_TIMER_TRIGGER = 'AGD_StartTrigger';  
    AGD_TD_PATCH_CONTROL = 'AGD_LaunchGeneration';
    AGD_TD_PATCH_CONTROL_EXEC = 'AGD_LaunchGeneration_exec'

#####################################################################
# Enum:         AGD_LengthUnits
# Enum Type:    IntEnum
# Description:  This enum contains integers that are used for
#                choosing timing method in Touch Designer
# Values:
#   LENGTH_UNIT_SAMPLES - Sample Count Mode
#   LENGTH_UNIT_FRAMES - Frame Count Mode
#   LENGTH_UNIT_SECONDS - Time Count Mode
#####################################################################
class AGD_LengthUnits(IntEnum):
    LENGTH_UNIT_SAMPLES = 0
    LENGTH_UNIT_FRAMES  = 1
    LENGTH_UNIT_SECONDS = 2

