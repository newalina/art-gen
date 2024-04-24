import git
from enum import IntEnum, StrEnum
from shutil import which
import os

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
#   LOGGING_PATH_BASE - Contains the directory where common logs are
#    to be written.
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
        return git_root.replace('/', '\\');

    #####################################################################
    # Method:       get_touch_designer_executable
    # Purpose:      Find the path to the Touch Designer executable on 
    #                the current machine. 
    # Requirements: N/A
    # Inputs:       None      
    # Outputs:      Path to the Touch Designer executable
    #####################################################################
    def get_touch_designer_executable():
        # Only works if TD is on the PATH of machine executing this command. Hopefully there is a better
        #  way to do this
        try:
            # Do some manipulation of string to cover any potential issues of
            #  spaces in path.
            return '"' + str(which("TouchDesigner")) + '"';
        except:
            print("ERROR: Failed to Find Touch Designer Executable. Is it on your PATH?");
            return None;

    ROOT_DIR = get_project_root(os.getcwd());
    TD_DIR = '\\code\\TouchDesigner';
    TD_EXEC = get_touch_designer_executable();
    LOGGING_PATH_BASE = ROOT_DIR + '\\code\\Backend\\Common\\logs\\'


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
    ERR_LEVEL_ERROR     = 0
    ERR_LEVEL_WARNING   = 1
    ERR_LEVEL_DEBUG     = 2
    ERR_LEVEL_TRACE     = 3
    ERR_LEVEL_ALL       = 4 



class CMN_LoggingDomain(IntEnum):
    CMN_LOG_DOMAIN_BE   = 0
    CMN_LOG_DOMAIN_TD   = 1
    CMN_LOG_DOMAIN_UT   = 2