##########################################################################
#
# File: AGD_Simulator.py
# 
# Purpose of File: The purpose of this file is to contain all of the 
#                   simulated drivers that act as a unit test for the
#                   basic functionality of running touch designer for
#                   various patches in various modes. 
#
# Creation Date: April 20th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import sys

# TODO: Remove this and generalize path loading
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/Common/src/')

# Private Modules
from AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from CMN_ErrorLogging import CMN_LoggingLevels as CMN_LL
from CMN_ErrorLogging import log

#####################################################################
# Function:     runBaselineTest
# Purpose:      The baseline test tests the basic functionality of
#                the Art Generation Driver without the use of user 
#                inputs to the queue. This test creates new art
#                units, performs art generation on a sample patch,
#                and outputs the art generation to a file. 
# Requirements: N/A
# Inputs:       None      
# Outputs:      None  
#####################################################################
def runBaselineTest():

    log.openFile();
    log.log(2, "AGD_Simulator.runBaselineTest() Starting runBaselineTest testcase");

    # Object 0
    testArtGenerator = AGD_ArtGeneratorUnit(0, 125, 32, 51);
    # Do some API stuff here
    testArtGenerator.updateArtGenerationData();
    testArtGenerator.writeToJSON();
    #testArtGenerator.startTouchDesigner();
    # Here do something with the data...
    log.log(2, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance 1");

    # Object 1
    test2 = AGD_ArtGeneratorUnit(0, 1, 24, 61);
    # Do some API stuff here
    test2.updateArtGenerationData();
    test2.writeToJSON();
    #test2.startTouchDesigner();
    # Here do something with the data...
    log.log(2, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance 2");

    log.log(2, "AGD_Simulator.runBaselineTest() Finishing runBaselineTest testcase");
    log.closeFile();



# TODO: Make a more robust simulation framework for each generation type
runBaselineTest();