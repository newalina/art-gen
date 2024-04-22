# This should probably be moved into Definitions. 

# Test file for Art Generation Driver
# Public Modules
from enum import Enum;

# Project Modules
from AGD_Definitions import AGD_Directories as AGD_DIR

# Tried initially as an enum, but I think a class may be better for getters, etc. Can always revert to Enum or whatever is 
#  best practice
class AGD_TouchDesignerPatch(Enum):

    #def __init__(Enum):
    TD_PATCH_NONE       = 0;
    TD_PATCH_RESERVED_1 = 1;
    TD_PATCH_RESERVED_2 = 2;
    TD_PATCH_RESERVED_3 = 3;
    TD_PATCH_RESERVED_4 = 4;
    TD_PATCH_RESERVED_5 = 5;
    TD_PATCH_RESERVED_6 = 6;
    TD_PATCH_RESERVED_7 = 7;
    TD_PATCH_RESERVED_8 = 8;
    TD_PATCH_MAX_PATCH  = 9;

    TD_PATCH_FILES      = ['"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\none.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\hex-quakes.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-2.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-3.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-4.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-5.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-6.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-7.toe"',
                           '"' + AGD_DIR.ROOT_DIR.value + AGD_DIR.TD_DIR.value + '\\Patches\\reserved-8.toe"']

    @classmethod
    def getPathToPatch(self, patchNumber):
        if(patchNumber < AGD_TouchDesignerPatch.TD_PATCH_MAX_PATCH.value):
            return list(AGD_TouchDesignerPatch.TD_PATCH_FILES.value)[patchNumber];
        else:
            print("ERROR: Cannot print");
            return -1;

#execStr = AGD_DIR.TD_EXEC.value + " " + AGD_TouchDesignerPatch.TD_PATCH_RESERVED_1.value;
#subprocess.run(execStr);




