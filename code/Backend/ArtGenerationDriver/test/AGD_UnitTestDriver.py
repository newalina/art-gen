##########################################################################
#
# File: AGD_UnitTestDriver.py
#
# Purpose of File: The purpose of this file is to act as a wrapper to 
#                   the unit test functionality implemented in the
#                   AGD_Simulator class. When run, this file prompts the
#                   user to enter in the tests that they want to run,
#                   and will execute the tests as requested. 
#
# Creation Date: April 30th, 2024
#
# Author: Alec Pratt
#
##########################################################################

# Project Includes
from Backend.ArtGenerationDriver.src.AGD_Definitions import AGD_Testcases as AGD_TC
from Backend.ArtGenerationDriver.test.AGD_Simulator import AGD_Simulator 
from Backend.Common.src.CMN_Definitions import CMN_LoggingLevels as CMN_LL
from Backend.Common.src.CMN_Definitions import CMN_LoggingDomain as CMN_LD
from Backend.Common.src.CMN_ErrorLogging import CMN_Logging

# Main Function
if __name__ == "__main__":

    print("*************************************************************")
    print("Starting Unit Test Driver for Art Generation Driver Functionality")
    print("To run test cases, input numbers one at a time that correspond to test cases")
    print("Enter 'x' once all desired test cases have been entered")
    print("Enter 'h' for a robust list of test cases\n")

    logFile = CMN_Logging(CMN_LL.ERR_LEVEL_DEBUG, CMN_LD.CMN_LOG_DOMAIN_UT);
    logFile.openFile();

    argsIn = set();
    while(True):
        val = input("Add test case (Input 'x' when finished, or 'h' for help): ");

        if(val == 'x' or val == 'X'):
            break;

        if(val == 'h' or val == 'H'):
            print("Help Menu for Art Generation Driver Unit Tests");
            print("**********************************************");
            print("Test Name\t\t   Number Input\n");
            print("Baseline Test\t\t\t0");
            print("Loop Test\t\t\t1");
            print("Shore Test\t\t\t2");
            print("Instance Test\t\t\t3");
            print("Hex Quake Test\t\t\t4");
            print("Watercolor Test\t\t\t5");
            print("Comprehensive Test\t\t6");
            print("\nNOTE: If the Comprehensive Test option is selected, only this test will run.");
        elif(val.isdigit()):
            if(int(val) < AGD_TC.AGD_TC_MAXIMUM):
                argsIn.add(int(val));
            else:
                print("ERROR: Invalid Parameter. To see valid input options, enter 'h'");
        else:
            print("ERROR: Invalid Parameter. To see valid input options, enter 'h'");
    
    sim = AGD_Simulator(list(argsIn), logFile);
    
    print("AGD_UT: Starting Unit Test Processing");
    sim.runTests();
    print("AGD_UT: Finished Unit Test Processing");
    print(f"AGD_UT: For debug information, check: {logFile.path_}");
    print("AGD_UT: Shutting down...");
    logFile.closeFile();
