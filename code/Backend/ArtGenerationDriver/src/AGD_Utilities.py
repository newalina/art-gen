##########################################################################
#
# File: AGD_Utilities.py
# 
# Purpose of File: The purpose of this file is to contain the utility
#					functions that are used in art generation processing
#					in Touch Designer. 
#
# Creation Date: April 14th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import td;
import sys;

#####################################################################
# Function:     onDone
# Purpose:      A function used by the timer tracking generation
#				 time in Touch Designer. This function is called to
#				 exit out of Touch Designer once procecssing has 
#				 finished.
# Requirements: N/A
# Inputs:       timerOp - No Idea
#				segment - No Idea
#				interrupt - No Idea     
# Outputs:      None  
#####################################################################
def onDone(timerOp, segment, interrupt):
	sys.stdout.write("TRACE: TouchDesigner Closing...\n");
	quit();
	return

#####################################################################
# Function:     onDone
# Purpose:      A function used by the execute CHOP on start-up that
#				 is used to start the actual processing of Touch
#				 Designer. 
# Requirements: N/A
# Inputs:       args - arguments passed into function by Touch Designer
# Outputs:      None  
#####################################################################
def onStart(*args):

	if(len(args) > 0):
		sys.stdout.write("ERROR: More than 0 args: " + str(args) + "\n");
	
	td.op("AGD_LaunchGeneration").run()