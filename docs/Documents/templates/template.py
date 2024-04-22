##########################################################################
#
# File: template.py
# 
# Purpose of File: The purpose of this file is to act as a template for
#                   the Python programming style guideline. This program
#                   may not run correctly, but the point was to show how
#                   to apply the guidelines that were mentioned in the
#                   official document.
#
# Creation Date: April 22nd, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
from random import randint 
from enum import IntEnum

# Project Modules
# from AGD_Definitions import AGD_Directories as AGD_DIR

# Class Definitions
class TMP_TemplateClass:

    # Unused variable to demonstrate naming convention
    counter_variable_ = 0;

    #####################################################################
    # Method:     __init__
    # Purpose:      Initialize a new instance of TMP_TemplateClass class
    # Requirements: REQ_1
    # Inputs:       self - current class member 
    # Outputs:      None  
    #####################################################################
    def __init__(self):
        self.integerAlpha_ = randint(TMP_RandomParameters.TMP_MIN_BOUND, TMP_RandomParameters.TMP_MAX_BOUND);
        self.integerBeta_ = randint(TMP_RandomParameters.TMP_MIN_BOUND, TMP_RandomParameters.TMP_MAX_BOUND);

        tempVariable = self.integerAlpha_ + self.integerBeta_;

        # REQ_1
        self.result = tempVariable;

    #####################################################################
    # Method:     compareToGlobal
    # Purpose:      Compare the class result to the global randint
    # Requirements: N/A
    # Inputs:       self - current class member 
    # Outputs:      None  
    #####################################################################
    def compareToGlobal(self):
        global RandomInteger;
        if(RandomInteger > self.result):
            print("A");
        else:
            print("B");

# Enum Definitions
#####################################################################
# Enum:         TMP_RandomParameters
# Enum Type:    IntEnum
# Description:  An enum containing the minimum and maximum range
#                for randint()
# Values:
#   TMP_MIN_BOUND - The minimum value for randint() range
#   TMP_MAX_BOUND - The maximum value for randint() range
#####################################################################
class TMP_RandomParameters(IntEnum):
    @classmethod
    def sample_enum_method():
        return 100;

    TMP_MIN_BOUND = 0;
    TMP_MAX_BOUND = sample_enum_method();



# Function Definitions
#####################################################################
# Function:     TemplateDriver
# Purpose:      Run the template program
# Requirements: N/A
# Inputs:       None
# Outputs:      None  
#####################################################################
def TemplateDriver():
    testClass = TMP_TemplateClass();
    testClass.compareToGlobal();

# Global Variable Definitions
RandomInteger = randint(TMP_RandomParameters.TMP_MIN_BOUND, TMP_RandomParameters.TMP_MAX_BOUND);

# Run Program
TemplateDriver();

