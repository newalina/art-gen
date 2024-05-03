##########################################################################
#
# File: CMN_Definitions.py
# 
# Purpose of File: The purpose of this file is to contain all defined
#                   values that are shared across the Art Generator
#                   Project. 
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import git
from enum import IntEnum, StrEnum
import os

#####################################################################
# Enum:         CMN_Directories
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
#   LOGGING_PATH_BASE - Contains the directory where common logs are
#    to be written.
#   LOGGING_PATH_BASE_UT - Contains the directory where unit test
#    logs are to be written. 
#####################################################################
class CMN_Directories(StrEnum):

    #####################################################################
    # Method:       get_project_root
    # Purpose:      Find the root of the github repo that this project
    #                is being run in. 
    # Requirements: N/A
    # Inputs:       path - The path to the current working directory.        
    # Outputs:      Path to root of GitHub Repository  
    #####################################################################
    def get_project_root(path):
        git_repo = git.Repo(path, search_parent_directories=True)
        git_root = str(git_repo.git.rev_parse("--show-toplevel"))

        # Do some manipulation of string to make it windows compatible
        return git_root.replace('/', '/');

    ROOT_DIR = get_project_root(os.getcwd());
    TD_DIR = '/code/TouchDesigner';
    TD_EXEC = 'TouchDesigner';
    LOGGING_PATH_BASE = ROOT_DIR + '/code/Backend/Common/logs/'
    LOGGING_PATH_BASE_UT = ROOT_DIR + '/code/Backend/ArtGenerationDriver/test/logs/'

#####################################################################
# Enum:         CMN_LoggingLevels
# Enum Type:    IntEnum
# Description:  This enum contains the logging levels that can be 
#                used in the Art Generator Project. Review the 
#                guide to learn about how to use these logging 
#                levels. 
# Values:
#   ERR_LEVEL_ERROR - Error Logging Level
#   ERR_LEVEL_WARNING - Warning Logging Level
#   ERR_LEVEL_DEBUG - Debug Logging Level
#   ERR_LEVEL_TRACE - Trace Logging Level
#   ERR_LEVEL_ALL - Logging level enabling all logging.              
#####################################################################
class CMN_LoggingLevels(IntEnum):
    ERR_LEVEL_ERROR     = 0;
    ERR_LEVEL_WARNING   = 1;
    ERR_LEVEL_DEBUG     = 2;
    ERR_LEVEL_TRACE     = 3;
    ERR_LEVEL_ALL       = 4;

#####################################################################
# Enum:         CMN_LoggingDomain
# Enum Type:    IntEnum
# Description:  This enum contains the logging domains that are used
#                for the logging class. This helps initialize the 
#                class properly to output the file to the correct
#                location with the correct naming convention
# Values:
#   CMN_LOG_DOMAIN_BE - Backend Logging (Run in main program)
#   CMN_LOG_DOMAIN_TD - Touch Designer Logging (TD Errors)
#   CMN_LOG_DOMAIN_UT - Unit Test Logging (Run in UT Driver)
#####################################################################
class CMN_LoggingDomain(IntEnum):
    CMN_LOG_DOMAIN_BE   = 0;
    CMN_LOG_DOMAIN_TD   = 1;
    CMN_LOG_DOMAIN_UT   = 2;

#####################################################################
# Enum:         CMN_ErrorCodes
# Enum Type:    IntEnum
# Description:  This enum contains the error codes that can be sent
#                and received by different functionalities of the
#                project code. 
# Values:
#   CMN_ERR_OK - No error
#   CMN_ERR_GENERIC - Generic error that can be used as a palceholder
#   CMN_ERR_INVALID_DATA - Invalid data passed as an argument
#####################################################################
class CMN_ErrorCodes(IntEnum):
    CMN_ERR_OK           = 0;
    CMN_ERR_GENERIC      = 1;
    CMN_ERR_INVALID_DATA = 2;

#####################################################################
# Enum:         CMN_StorageMonitorErrorCode
# Enum Type:    IntEnum
# Description:  This enum contains the error codes that can be sent
#                and received by the storage monitor.
# Values:
#   SM_ERROR_CODE_OK - No error
#   SM_ERROR_CODE_FULL - Storage is full
#####################################################################
    
class CMN_StorageMonitorErrorCode(IntEnum):
    SM_ERROR_CODE_OK = 0;
    SM_ERROR_CODE_FULL = 0;