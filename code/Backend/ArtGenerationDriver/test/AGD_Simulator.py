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

# Project Modules
from Backend.ArtGenerationDriver.src.AGD_ArtGeneratorUnit import AGD_ArtGeneratorUnit
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TouchDesignerPatch as AGD_TDP
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Testcases as AGD_TC
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_TESTCASE_METHODS
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging


class AGD_Simulator:

    #####################################################################
    # Method:       __init__
    # Purpose:      Initialize a new instance of the AGD_Simulator
    #                class. 
    # Requirements: N/A
    # Inputs:       self - current class member
    #               args - A list of tests to run that is created in the
    #                unit test driver.
    #               logger - A reference to the logging object that
    #                stores all logging information for this unit test
    #                execution. 
    # Outputs:      None  
    #####################################################################
    def __init__(self, args, logger):
        self.logger_ = logger;
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.__init__() in");

        # Initialize class members
        self.numberOfTests_ = len(args);
        self.testsToRun_ = self.createTestQueue(args);

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.__init__() out");
    
    #####################################################################
    # Method:       createTestQueue
    # Purpose:      This method creates the test queue that is used to
    #                call all of the tests requested by the user.
    # Requirements: N/A
    # Inputs:       self - current class member
    #               tests - A list of tests that should be run
    # Outputs:      None  
    #####################################################################
    def createTestQueue(self, tests):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.createTestQueue() in");

        testQueue = [];

        for idx in range(self.numberOfTests_):
            if(tests[idx] == AGD_TC.AGD_TC_COMPREHENSIVE):
                self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.createTestQueue() Comprehensive test selected. Resetting queue and only running comprehensive test"); 
                testQueue.clear();
                testQueue.append(AGD_TESTCASE_METHODS[AGD_TC.AGD_TC_COMPREHENSIVE]);
                return testQueue;
            else:
                self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, f"AGD_Simulator.createTestQueue() Adding {AGD_TESTCASE_METHODS[tests[idx]]} to test queue");  
                testQueue.append(AGD_TESTCASE_METHODS[tests[idx]]);

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.createTestQueue() out");              
        return testQueue;

    #####################################################################
    # Method:       runTests
    # Purpose:      This method runs the entire test suite that is
    #                selected by the user. 
    # Requirements: N/A
    # Inputs:       self - current class member  
    # Outputs:      None  
    #####################################################################
    def runTests(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runTests() in");   

        for test in self.testsToRun_:
            self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, f"AGD_Simulator.runTests() Starting test: {test}");   
            exec(f"self.{test}()")

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runTests() out");   

    #####################################################################
    # Method:       runBaselineTest
    # Purpose:      The baseline test tests the basic functionality of
    #                the Art Generation Driver without the use of user 
    #                inputs to the queue. This test creates new art
    #                units, performs art generation on a sample patch,
    #                and outputs the art generation to a file. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runBaselineTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Starting runBaselineTest testcase");

        # Initialize Parameters
        paramA = 125;
        paramB = 32;
        paramC = 51;
        paramD = None;
        paramE = None;
        paramF = None;

        # Object 0
        testGeneration1 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        testGeneration1.updateArtGenerationData();
        testGeneration1.writeToJSON();
        testGeneration1.startTouchDesigner();
        # Here do something with the data...
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration1.instance_id_));

        # Initialize Parameters
        paramA = 1;
        paramB = 2;
        paramC = 4;
        paramD = None;
        paramE = None;
        paramF = None;

        # Object 1
        testGeneration2 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        testGeneration2.updateArtGenerationData();
        testGeneration2.writeToJSON();
        testGeneration2.startTouchDesigner();
        # Here do something with the data...
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runBaselineTest() Succesfully Quit Instance " + str(testGeneration2.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runBaselineTest() Finishing runBaselineTest testcase");

    #####################################################################
    # Method:       runLoopTest
    # Purpose:      This test confirms that the 'loop' patch can properly
    #                be run with Python inputs and with a proper file
    #                output. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runLoopTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runLoopTest() Starting runLoopTest testcase");   

        # Initialize Parameters
        paramA = 6;
        paramB = 10;
        paramC = 0.1;
        paramD = 1.8
        paramE = 0xfe52d0;
        paramF = None;

        # Object 0
        loopGeneration0 = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_LOOP.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        loopGeneration0.updateArtGenerationData();
        loopGeneration0.writeToJSON();
        loopGeneration0.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runLoopTest() Succesfully Quit Instance " + str(loopGeneration0.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runLoopTest() Finishing runLoopTest testcase");

    #####################################################################
    # Method:       runShoreTest
    # Purpose:      This test confirms that the 'shore' patch can 
    #                properly be run with Python inputs and with a proper 
    #                file output. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runShoreTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runShoreTest() Starting runShoreTest testcase");   

        # Initialize Parameters
        paramA = 4;
        paramB = 1.4;
        paramC = 14;
        paramD = 0xa76b10;
        paramE = None;
        paramF = None;

        # Object 0
        shoreGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_SHORE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        shoreGeneration.updateArtGenerationData();
        shoreGeneration.writeToJSON();
        shoreGeneration.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runShoreTest() Succesfully Quit Instance " + str(shoreGeneration.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runShoreTest() Finishing runShoreTest testcase");


    #####################################################################
    # Method:       runInstanceTest
    # Purpose:      This test confirms that the 'instance' patch can 
    #                properly be run with Python inputs and with a proper 
    #                file output. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runInstanceTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runInstanceTest() Starting runInstanceTest testcase");   

        # Initialize Parameters
        paramA = 6;
        paramB = 5;
        paramC = 0.9;
        paramD = None;
        paramE = None;
        paramF = None;

        # Object 0
        instanceGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_INSTANCE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        instanceGeneration.updateArtGenerationData();
        instanceGeneration.writeToJSON();
        instanceGeneration.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runInstanceTest() Succesfully Quit Instance " + str(instanceGeneration.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runInstanceTest() Finishing runInstanceTest testcase");
    
    #####################################################################
    # Method:       runHexQuakeTest
    # Purpose:      This test confirms that the 'hex_quake' patch can 
    #                properly be run with Python inputs and with a proper 
    #                file output. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runHexQuakeTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runHexQuakeTest() Starting runHexQuakeTest testcase");   

        # Initialize Parameters
        paramA = 2;
        paramB = 6;
        paramC = 0.6;
        paramD = 0x641f52;
        paramE = None;
        paramF = None;

        # Object 0
        particleGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_HEX_QUAKE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        particleGeneration.updateArtGenerationData();
        particleGeneration.writeToJSON();
        particleGeneration.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runHexQuakeTest() Succesfully Quit Instance " + str(particleGeneration.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runHexQuakeTest() Finishing runHexQuakeTest testcase");
    
    #####################################################################
    # Method:       runWatercolorTest
    # Purpose:      This test confirms that the 'watercolor' patch can 
    #                properly be run with Python inputs and with a proper 
    #                file output. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runWatercolorTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runWatercolorTest() Starting runWatercolorTest testcase");   

        # Initialize Parameters
        paramA = 0.0001;
        paramB = 0.001;
        paramC = 0.999;
        paramD = 42;
        paramE = None;
        paramF = None;

        # Object 0
        watercolorGeneration = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_WATERCOLOR.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        watercolorGeneration.updateArtGenerationData();
        watercolorGeneration.writeToJSON();
        watercolorGeneration.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runWatercolorTest() Succesfully Quit Instance " + str(watercolorGeneration.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runWatercolorTest() Finishing runWatercolorTest testcase");
    
    #####################################################################
    # Method:       runComprehensiveTest
    # Purpose:      This test is a comprehensive test suite that tests 
    #                every patch associated with the Art Generation 
    #                Project. 
    # Requirements: N/A
    # Inputs:       self - current class member      
    # Outputs:      None  
    #####################################################################
    def runComprehensiveTest(self):
        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runComprehensiveTest() Starting runComprehensiveTest testcase");

        # Initialize Parameters
        paramA = 6;
        paramB = 10;
        paramC = 0.1;
        paramD = 1.8
        paramE = 0xfe52d0;
        paramF = None;

        # Object 0 - 'None'
        genNone = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_NONE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genNone.updateArtGenerationData();
        genNone.writeToJSON();
        genNone.startTouchDesigner();
        # Here do something with the data...
        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genNone.instance_id_));

        # Initialize Parameters
        paramA = 6;
        paramB = 10;
        paramC = 0.1;
        paramD = 1.8
        paramE = 0xfe52d0;
        paramF = None;

        # Object 1 - 'Loop'
        genLoop = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_LOOP.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genLoop.updateArtGenerationData();
        genLoop.writeToJSON();
        genLoop.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genLoop.instance_id_));

        # Initialize Parameters
        paramA = 4;
        paramB = 1.4;
        paramC = 14;
        paramD = 0xa76b10;
        paramE = None;
        paramF = None;

        # Object 2 - 'Shore'
        genShore = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_SHORE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genShore.updateArtGenerationData();
        genShore.writeToJSON();
        genShore.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genShore.instance_id_));

        # Initialize Parameters
        paramA = 6;
        paramB = 5;
        paramC = 0.9;
        paramD = None;
        paramE = None;
        paramF = None;

        # Object 3 - 'Instance'
        genInstance = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_INSTANCE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genInstance.updateArtGenerationData();
        genInstance.writeToJSON();
        genInstance.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genInstance.instance_id_));

        # Initialize Parameters
        paramA = 2;
        paramB = 6;
        paramC = 0.6;
        paramD = 0x641f52;
        paramE = None;
        paramF = None;

        # Object 4 - 'Hex Quake'
        genParticle = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_HEX_QUAKE.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genParticle.updateArtGenerationData();
        genParticle.writeToJSON();
        genParticle.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genParticle.instance_id_));

        # Initialize Parameters
        paramA = 0.0001;
        paramB = 0.001;
        paramC = 0.999;
        paramD = 42;
        paramE = None;
        paramF = None;

        # Object 5 - 'Watercolor'
        genWatercolor = AGD_ArtGeneratorUnit(AGD_TDP.TD_PATCH_WATERCOLOR.value, paramA, paramB, paramC, paramD, paramE, paramF, self.logger_);
        # Do some API stuff here
        genWatercolor.updateArtGenerationData();
        genWatercolor.writeToJSON();
        genWatercolor.startTouchDesigner();

        self.logger_.log(CMN_LL.ERR_LEVEL_DEBUG, "AGD_Simulator.runComprehensiveTest() Succesfully Quit Instance " + str(genWatercolor.instance_id_));

        self.logger_.log(CMN_LL.ERR_LEVEL_TRACE, "AGD_Simulator.runComprehensiveTest() Finishing runComprehensiveTest testcase");