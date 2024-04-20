from enum import IntEnum
import sys

from datetime import datetime

# Create a script that properly adds all python scripts. 
#sys.path.insert(0, ""



#from AGD_Definitions import AGD_Directories as AGD_DIR


def createTime():
    currTime = datetime.now();
    return str(currTime.year) + '-' + str(currTime.month) + '-' + str(currTime.day) + '-' \
           + str(currTime.hour) + '.' + str(currTime.minute) + '.' + str(currTime.second) + '.' + str(currTime.microsecond);





class CMN_LoggingLevels(IntEnum):
    ERR_LEVEL_ERROR     = 0
    ERR_LEVEL_WARNING   = 1
    ERR_LEVEL_DEBUG     = 2
    ERR_LEVEL_ALL       = 3 

LOG_PATH = "c:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\Common\\" + createTime() + "_runLog.log";

print(LOG_PATH)

