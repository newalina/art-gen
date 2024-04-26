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

# Private Modules
from Backend.ArtGenerationDriver.src.AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging

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

    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Starting runBaselineTest testcase");

    # Object 0
    testGeneration1 = AGD_ArtGeneratorUnit(0, 125, 32, 51, log);
    # Do some API stuff here
    testGeneration1.updateArtGenerationData();
    testGeneration1.writeToJSON();
    testGeneration1.startTouchDesigner();
    # Here do something with the data...
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration1.instance_id_));

    # Object 1
    testGeneration2 = AGD_ArtGeneratorUnit(0, 1, 24, 61, log);
    # Do some API stuff here
    testGeneration2.updateArtGenerationData();
    testGeneration2.writeToJSON();
    testGeneration2.startTouchDesigner();
    # Here do something with the data...
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration2.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Finishing runBaselineTest testcase");
    log.closeFile();



# TODO: Make a more robust simulation framework for each generation type
runBaselineTest();