##########################################################################
#
# File: TD_InitializePatch.py
# 
# Purpose of File: The purpose of this file is to initialize Touch 
#                   Designer to utilize the appropriate project specific
#                   paths for the control scheme and to start the process
#                   of art generation.
#
#                   NOTE: This file must manually be loaded into Touch
#                    Designer. It cannot be loaded in at run-time
#
# Creation Date: April 13th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import td
import sys
from pathlib import Path

# TODO: Find a better way to do this
#sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/ArtGenerationDriver/src/')

# Private Modules
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD

# Continue working on this
TDLog = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_TD);

#####################################################################
# Function:     onOffToOn
# Purpose:      A function used by Touch Designer to initialize the
#                patch with proper paths to Python files. 
# Requirements: N/A
# Inputs:       channel - No Idea
#				sampleIndex - No Idea
#				val - No Idea     
#               prev - No Idea
# Outputs:      None  
#####################################################################
def onOffToOn(channel, sampleIndex, val, prev):
    sys.stdout.write("Init: " + TDLog.path_ + "\n");

    sys.stdout.write("Initialize New Patch\n");
    # Load in Patch Control File 
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL).par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_LaunchGeneration.py';
    td.op("AGD_LaunchGeneration_exec").par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_Utilities.py';
    td.op("AGD_TimerCallbacks").par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_Utilities.py';

    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL).par.loadonstartpulse.pulse()
    td.op("AGD_LaunchGeneration_exec").par.loadonstartpulse.pulse()
    td.op("AGD_TimerCallbacks").par.loadonstartpulse.pulse()

    # Start Execution
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL_EXEC).par.startpulse.pulse()
    return
