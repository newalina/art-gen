##########################################################################
#
# File: BCI_Definitions.py
# 
# Purpose of File: The purpose of this file is to contain all defined
#                   values that are used in the Back End Command
#                   Interface.
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
from enum import StrEnum, IntEnum

# Project Modules
from Backend.Common.src.CMN_Definitions import CMN_Directories as CMN_DIR

# TODO: Enums for video/<video type>, for strings, or hardcoded urls

#####################################################################
# Enum:         BCI_Directories
# Enum Type:    StrEnum
# Description:  This enum contains different paths or urls that are 
#                necessary for the Back End Command Interface. 
# Values:
#   BCI_DATA_DIR - Data directory of Back End Command Interface
#   BCI_OUTPUT_FILE_BASE - File output base for sending data to
#    front-end. 
#   BCI_MONGO_URI - URL to mongoDb server. 
#####################################################################
class BCI_Directories(StrEnum):
    BCI_DATA_DIR         = CMN_DIR.ROOT_DIR + '/code/Backend/BackEndCommandInterface/data'
    BCI_OUTPUT_FILE_BASE = BCI_DATA_DIR + '/artGenerationOutput_'
    BCI_MONGO_URI        = 'mongodb+srv://malique-bodie:86zb67pNK3U3BgEt@art-gen.bxqjsqp.mongodb.net/?retryWrites=true&w=majority'

#####################################################################
# Enum:         BCI_ErrorCodes
# Enum Type:    IntEnum
# Description:  This enum contains all error codes that the Flask
#                server will intentionally send from our design
# Values:
#   BCI_ERR_200 - Error Code for OK
#   BCI_ERR_500 - Error Code for generic error
#####################################################################
class BCI_ErrorCodes(IntEnum):
    BCI_ERR_200 = 200;
    BCI_ERR_500 = 500;

#####################################################################
# List:         ENVIRONMENT_API
# Description:  This list contains links to all environemnt API
#####################################################################
ENVIRONTMENT_API = {
        'Carbon Dioxide' : 'https://global-warming.org/api/co2-api',
        'Methane' : 'https://global-warming.org/api/methane-api',
        'Nitrous Oxide' : 'https://global-warming.org/api/nitrous-oxide-api',
        'Ocean Temperature' : 'https://global-warming.org/api/ocean-warming-api',
        'Sea Ice Extent' : "https://global-warming.org/api/arctic-api"
    }

MODEL_RANGES = {
    '1': [
        (0.0001, 0.001),
        (0.0001, 0.001),
        (0.999, 1),
        (0, 100)
    ],

    '2': [
        (1, 8),
        (1, 5),
        (0.1, 1)
    ],

    '3' : [
        (6, 10),
        (0.1, 0.5),
    ],
    '4': [
        (1, 3),
        (0.1,10),
        (0.1, 0.7),
    ],
    '5': [
        (1, 5),
        (0.1, 3),
        (0, 100),
    ]
}
