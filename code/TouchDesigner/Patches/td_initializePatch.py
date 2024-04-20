# File loaded in by chop execute DAT object in TD. This is used to laod 
#  in and execute every touch designer patch 

# This patch has to be manually loaded into TD using 'pulse'. It cannot be loaded in during run time, because it causes problems with loading in the other needed
#  files. 


# There has got to be a better way to get the paths set up. Either inside of TD, or another script that can be run so TD will recognize this stuff.
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/ArtGenerationDriver/src/')

import td
import sys
from pathlib import Path

from AGD_Definitions import AGD_TouchDesignerNodes as AGD_TDN

# Callback function used for CHOP Execute DAT. 
def onOffToOn(channel, sampleIndex, val, prev):

    # Load in Patch Control File 
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL).par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_LaunchGeneration.py';
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL_EXEC).par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_Utilities.py';
    td.op(AGD_TDN.AGD_TD_TIMER_CALLBACK_NODE).par.file = 'C:\\Users\\pratt\\Documents\\Academics\\Brown University\\Courses\\SP2024\\CSCI2340\\FinalProject\\art-gen\\code\\Backend\\ArtGenerationDriver\\src\\AGD_Utilities.py';

    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL).par.loadonstartpulse.pulse()
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL_EXEC).par.loadonstartpulse.pulse()
    td.op(AGD_TDN.AGD_TD_TIMER_CALLBACK_NODE).par.loadonstartpulse.pulse()

    # Start Execution
    td.op(AGD_TDN.AGD_TD_PATCH_CONTROL_EXEC).par.startpulse.pulse()
    return
