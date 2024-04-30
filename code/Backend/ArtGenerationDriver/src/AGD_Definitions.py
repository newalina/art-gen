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
from enum import StrEnum, IntEnum, Enum
from shutil import which

# Project Modules
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR

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
#   AGD_DATA_DIR - Contains the path to the Art Generation Driver 
#    data directory
#   AGD_INPUT_JSON - Contains the path to the Art Generation Driver
#    input JSON file
#   AGD_OUTPUT_JSON - Contains the path to the Art Generation Driver
#    output JSON file
#   AGD_OUTPUT_FILE_BASE - Provides a string that is the base of any
#    art generation output file
#####################################################################
class AGD_Directories(StrEnum):
    AGD_SRC_DIR = CMN_DIR.ROOT_DIR + '/code/Backend/ArtGenerationDriver/src'
    AGD_DATA_DIR = CMN_DIR.ROOT_DIR + '/code/Backend/ArtGenerationDriver/data';
    AGD_INPUT_JSON = AGD_DATA_DIR + '/artGenerationDataInput.json';
    AGD_OUTPUT_JSON = AGD_DATA_DIR + '/artGenerationDataOutput.json';
    AGD_OUTPUT_FILE_BASE = AGD_DATA_DIR + '/artGenerationOutput_';


#####################################################################
# Enum:         AGD_RecordingParameters
# Enum Type:    IntEnum
# Description:  This enum contains integers that are used for
#                adjusting recording parameters in Touch Designer.
# Values:
#   AGD_RECORDING_OFF - Disables recording in Touch Designer
#   AGD_RECORDING_ON - Enables recording in Touch Designer
#   AGD_RECORDING_DURATION - Duration of Touch Designer output (s)
#   AGD_RECORDING_DELAY - Duration of a delay introduced to prevent
#    any corruption of recording video files. 
#####################################################################
class AGD_RecordingParameters(IntEnum):
    AGD_RECORDING_OFF = 0;
    AGD_RECORDING_ON = 1;
    AGD_RECORDING_DURATION = 5;
    AGD_RECORDING_DELAY = 1;

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
#   LENGTH_UNIT_FRACTION = Fraction Count Mode
#####################################################################
class AGD_LengthUnits(IntEnum):
    LENGTH_UNIT_SAMPLES = 0
    LENGTH_UNIT_FRAMES  = 1
    LENGTH_UNIT_SECONDS = 2
    LENGTH_UNIT_FRACTION = 3

#####################################################################
# Enum:         AGD_TouchDesignerPatch
# Enum Type:    Enum
# Description:  This enum contains the different patches that can
#                be run in Touch Designer.  
# Values:
#   TD_PATCH_NONE - No Patch
#   TD_PATCH_RESERVED_1 - Reserved Patch 1
#   TD_PATCH_RESERVED_2 - Reserved Patch 2
#   TD_PATCH_RESERVED_3 - Reserved Patch 3
#   TD_PATCH_RESERVED_4 - Reserved Patch 4
#   TD_PATCH_RESERVED_5 - Reserved Patch 5
#   TD_PATCH_RESERVED_6 - Reserved Patch 6
#   TD_PATCH_RESERVED_7 - Reserved Patch 7
#   TD_PATCH_RESERVED_8 - Reserved Patch 8
#   TD_PATCH_MAX_PATCH - Maximum Patch Number
#   TD_PATCH_FILES - List of paths to the patches
#####################################################################
class AGD_TouchDesignerPatch(Enum):

    #def __init__(Enum):
    TD_PATCH_NONE       = 0;
    TD_PATCH_LOOP       = 1;
    TD_PATCH_SHORE      = 2;
    TD_PATCH_INSTANCE   = 3;
    TD_PATCH_HEX_QUAKE  = 4;
    TD_PATCH_WATERCOLOR = 5;
    TD_PATCH_RESERVED_6 = 6;
    TD_PATCH_RESERVED_7 = 7;
    TD_PATCH_RESERVED_8 = 8;
    TD_PATCH_MAX_PATCH  = 9;

    TD_PATCH_FILES      = ['"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/none.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/loop.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/shore.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/instance.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/hex_quake.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/watercolour.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/reserved-6.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/reserved-7.toe"',
                           '"' + str(CMN_DIR.ROOT_DIR) + str(CMN_DIR.TD_DIR) + '/patches/reserved-8.toe"']

    @classmethod
    def getPathToPatch(self, patchNumber):
        # if(patchNumber < AGD_TouchDesignerPatch.TD_PATCH_MAX_PATCH.value):
        #     return list(AGD_TouchDesignerPatch.TD_PATCH_FILES.value)[patchNumber];
        # else:
        #     print("ERROR: Cannot print");
        #     return -1;
        try:
            return list(AGD_TouchDesignerPatch.TD_PATCH_FILES.value)[patchNumber];
        except:
            #log.log(CMN_LL.ERR_LEVEL_ERROR, "AGD_TouchDesignerPatch.getPathToPatch() Unsupported Patch Number")
            return -1;


# Count of # of args needed for each init type
class AGD_UnitInitializationTypes(IntEnum):
    AGD_UIT_DATA = 5
    AGD_UIT_JSON = 1



class AGD_VideoCodecTypes(IntEnum):
    AGD_CODEC_ANIMATION = 0
    AGD_CODEC_PHOTO_MOTION_JPEG = 1
    AGD_CODEC_MPEG4_PART2 = 2
    AGD_CODEC_H264 = 3
    AGD_CODEC_GOPRO = 4
    AGD_CODEC_HAP = 5
    AGD_CODEC_H265 = 6
    AGD_CODEC_GIF = 7
    AGD_CODEC_NOTCHLC = 8
    AGD_CODEC_VP8 = 9
    AGD_CODEC_VP9 = 10
    AGD_CODEC_APPLE_PRORES = 11



class AGD_Testcases(IntEnum):
    AGD_TC_BASELINE      = 0
    AGD_TC_LOOP          = 1
    AGD_TC_SHORE         = 2
    AGD_TC_INSTANCE      = 3
    AGD_TC_HEXQUAKE      = 4
    AGD_TC_WATERCOLOR    = 5
    AGD_TC_COMPREHENSIVE = 6
    AGD_TC_MAXIMUM       = 7


AGD_TESTCASE_METHODS = [ 'runBaselineTest', 'runLoopTest', 'runShoreTest', 'runInstanceTest', 'runHexQuakeTest', 'runWatercolorTest', 'runComprehensiveTest'];
