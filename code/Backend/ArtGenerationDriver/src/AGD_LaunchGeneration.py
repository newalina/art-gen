##########################################################################
#
# File: AGD_LaunchGeneration.py
# 
# Purpose of File: The purpose of this file is to start art generation
#                   in Touch Designer. This is a small script used to 
#                   interface with Touch Designer, so there is no formal 
#                   class / function. 
#
# Creation Date: April 14th, 2024
#
# Author: Alec Pratt
#       
##########################################################################

# Public Modules
import sys
 
# Project Modules
from Backend.ArtGenerationDriver.src.AGD_TouchDesignerInstance import AGD_TouchDesignerInstance;

# Confirm this works in touch designer
artGenInstance = AGD_TouchDesignerInstance();

# TODO: Make logging functionality work for TD
sys.stdout.write("\n\n***Starting New Instance***\n");
sys.stdout.write("Launch Gen for: " + str(artGenInstance.artDriverID_) + "\n")

artGenInstance.run();