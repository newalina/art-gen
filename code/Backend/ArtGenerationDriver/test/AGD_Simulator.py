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
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging





#####################################################################
# Function:     runComprehensiveTest
# Purpose:      This test is a comprehensive test suite that tests 
#                every patch associated with the Art Generation 
#                Project. 
# Requirements: N/A
# Inputs:       None      
# Outputs:      None  
#####################################################################
def runComprehensiveTest():
    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Starting runBaselineTest testcase");

    # Object 0 - 'None'
    genNone = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, 125, 32, 51, log);
    # Do some API stuff here
    genNone.updateArtGenerationData();
    genNone.writeToJSON();
    genNone.startTouchDesigner();
    # Here do something with the data...
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(genNone.instance_id_));

    # Object 1 - 'Loop'
    genLoop = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_LOOP.value, 125, 32, 51, log);
    # Do some API stuff here
    genLoop.updateArtGenerationData();
    genLoop.writeToJSON();
    genLoop.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runLoopTest() Succesfully Quit Instance " + str(genLoop.instance_id_));

    # Object 2 - 'Shore'
    genShore = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_SHORE.value, 125, 32, 51, log);
    # Do some API stuff here
    genShore.updateArtGenerationData();
    genShore.writeToJSON();
    genShore.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runShoreTest() Succesfully Quit Instance " + str(genShore.instance_id_));

    # Object 3 - 'Instance'
    genInstance = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_INSTANCE.value, 125, 32, 51, log);
    # Do some API stuff here
    genInstance.updateArtGenerationData();
    genInstance.writeToJSON();
    genInstance.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runInstanceTest() Succesfully Quit Instance " + str(genInstance.instance_id_));

    # Object 4 - 'Particle'
    genParticle = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_PARTICLE.value, 125, 32, 51, log);
    # Do some API stuff here
    genParticle.updateArtGenerationData();
    genParticle.writeToJSON();
    genParticle.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runParticleTest() Succesfully Quit Instance " + str(genParticle.instance_id_));

    # Object 5 - 'Watercolor'
    genWatercolor = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_WATERCOLOR.value, 125, 32, 51, log);
    # Do some API stuff here
    genWatercolor.updateArtGenerationData();
    genWatercolor.writeToJSON();
    genWatercolor.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runWatercolorTest() Succesfully Quit Instance " + str(genWatercolor.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runLoopTest() Finishing runLoopTest testcase");
    log.closeFile();

    return




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
    testGeneration1 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, 125, 32, 51, log);
    # Do some API stuff here
    testGeneration1.updateArtGenerationData();
    testGeneration1.writeToJSON();
    testGeneration1.startTouchDesigner();
    # Here do something with the data...
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration1.instance_id_));

    # Object 1
    testGeneration2 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, 1, 24, 61, log);
    # Do some API stuff here
    testGeneration2.updateArtGenerationData();
    testGeneration2.writeToJSON();
    testGeneration2.startTouchDesigner();
    # Here do something with the data...
    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration2.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Finishing runBaselineTest testcase");
    log.closeFile();

#####################################################################
# Function:     runLoopTest
# Purpose:      This test confirms that the 'loop' patch can properly
#                be run with Python inputs and with a proper file
#                output. 
# Requirements: N/A
# Inputs:       None      
# Outputs:      None  
#####################################################################
def runLoopTest():

    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runLoopTest() Starting runLoopTest testcase");   

    # Object 0
    loopGeneration0 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_LOOP.value, 125, 32, 51, log);
    # Do some API stuff here
    loopGeneration0.updateArtGenerationData();
    loopGeneration0.writeToJSON();
    loopGeneration0.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runLoopTest() Succesfully Quit Instance " + str(loopGeneration0.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runLoopTest() Finishing runLoopTest testcase");
    log.closeFile();



def runShoreTest():
    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runShoreTest() Starting runLoopTest testcase");   

    # Object 0
    shoreGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_SHORE.value, 125, 32, 51, log);
    # Do some API stuff here
    shoreGeneration.updateArtGenerationData();
    shoreGeneration.writeToJSON();
    shoreGeneration.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runShoreTest() Succesfully Quit Instance " + str(shoreGeneration.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runShoreTest() Finishing runShoreTest testcase");
    log.closeFile();


def runInstanceTest():
    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runInstanceTest() Starting runLoopTest testcase");   

    # Object 0
    instanceGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_INSTANCE.value, 125, 32, 51, log);
    # Do some API stuff here
    instanceGeneration.updateArtGenerationData();
    instanceGeneration.writeToJSON();
    instanceGeneration.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runInstanceTest() Succesfully Quit Instance " + str(instanceGeneration.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runInstanceTest() Finishing runInstanceTest testcase");
    log.closeFile();

def runParticleTest():
    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runParticleTest() Starting runLoopTest testcase");   

    # Object 0
    particleGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_PARTICLE.value, 125, 32, 51, log);
    # Do some API stuff here
    particleGeneration.updateArtGenerationData();
    particleGeneration.writeToJSON();
    particleGeneration.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runParticleTest() Succesfully Quit Instance " + str(particleGeneration.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runParticleTest() Finishing runParticleTest testcase");
    log.closeFile();   

def runWatercolorTest():
    log = CMN_Logging(CMN_LL.ERR_LEVEL_ALL, CMN_LD.CMN_LOG_DOMAIN_UT);
    log.openFile();
    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runWatercolorTest() Starting runLoopTest testcase");   

    # Object 0
    watercolorGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_WATERCOLOR.value, 125, 32, 51, log);
    # Do some API stuff here
    watercolorGeneration.updateArtGenerationData();
    watercolorGeneration.writeToJSON();
    watercolorGeneration.startTouchDesigner();

    log.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runWatercolorTest() Succesfully Quit Instance " + str(watercolorGeneration.instance_id_));

    log.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runWatercolorTest() Finishing runWatercolorTest testcase");
    log.closeFile(); 


# TODO: Make a more robust simulation framework for each generation type
# runBaselineTest();
# runLoopTest();
# runShoreTest();
# runInstanceTest();
# runParticleTest();
runWatercolorTest();