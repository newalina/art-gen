# INSTEAD OF DOING THIS IN A SEPARATE FILE, I CAN TURN THE CONTENTS OF THIS FILE INTO A FUNCTION IN AGD_Utilities.py. HERE, I CAN JUST INSERT MY
#  DESIRED LOGIC INTO the onStart FUNCTION USED IN AGD_launchGeneration_exec. THIS REDUCES FILE COUNT WITH LIKE 2 LINES OF CODE IN IT. 




# Public Modules
import sys
import td
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/ArtGenerationDriver/src/')
# THIS SHOULD PROBABLY BE CALLED PATCH CONTROl    

# Project Modules
from AGD_TouchDesignerInstance import AGD_TouchDesignerInstance;

artGenInstance = AGD_TouchDesignerInstance();
    
sys.stdout.write("\n\n***Starting New Instance***\n");

sys.stdout.write("Launch Gen for: " + str(artGenInstance.artDriverID) + "\n")

artGenInstance.run();