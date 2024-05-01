from enum import StrEnum

# Project Modules
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR

class BCI_Directories(StrEnum):
    BCI_DATA_DIR = CMN_DIR.ROOT_DIR + '/code/Backend/BackEndCommandInterface/data'
    BCI_OUTPUT_FILE_BASE = BCI_DATA_DIR + '/artGenerationOutput_'

# Enums for video/<video type>

# Enums for strings or hardcoded urls