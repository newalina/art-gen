
from enum import IntEnum




class CMN_StorageMonitorErrorCode(IntEnum):
    SM_ERROR_CODE_OK = 0
    SM_ERROR_CODE_FULL = 0


class CMN_StorageMonitor:

    def __init__(self, errorLogDirectory, artDataDirectory):

        self.errorLogDirectory = errorLogDirectory;
        self.artDataDirectory = artDataDirectory;

        return 0;

    def monitorDebugLogDictory(self):
        
        return 0;