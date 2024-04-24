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

# INSTEAD OF DOING THIS IN A SEPARATE FILE, I CAN TURN THE CONTENTS OF THIS FILE INTO A FUNCTION IN AGD_Utilities.py. HERE, I CAN JUST INSERT MY
#  DESIRED LOGIC INTO the onStart FUNCTION USED IN AGD_launchGeneration_exec. THIS REDUCES FILE COUNT WITH LIKE 2 LINES OF CODE IN IT. 

# Public Modules
import sys
import td
# TODO: Remove the need for adding sys path
#sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/ArtGenerationDriver/src/')
 
# THIS SHOULD PROBABLY BE CALLED PATCH CONTROl   
# Project Modules
from Backend.ArtGenerationDriver.src.AGD_TouchDesignerInstance import AGD_TouchDesignerInstance;

# Confirm this works in touch designer
artGenInstance = AGD_TouchDesignerInstance();

sys.stdout.write("\n\n***Starting New Instance***\n");

sys.stdout.write("Launch Gen for: " + str(artGenInstance.artDriverID_) + "\n")

artGenInstance.run();

sys.stdout.write("In Launch Generation\n");