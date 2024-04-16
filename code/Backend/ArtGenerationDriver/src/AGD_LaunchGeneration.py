# Public Modules
import sys
from time import sleep

# There has got to be a better way to get the paths set up. Either inside of TD, or another script that can be run so TD will recognize this stuff.
sys.path.insert(0, 'c:/Users/pratt/Documents/Academics/Brown University/Courses/SP2024/CSCI2340/FinalProject/art-gen/code/Backend/ArtGenerationDriver/src/')

# Project Modules
from AGD_ArtGenerator import AGD_ArtGenerator;




# sys.stdout.write();

def run():
    global artGenInstance


    sys.stdout.write("ID: " + str(artGenInstance.instance_id_) + ", X: " + str(artGenInstance.paramX) + \
                     ", Y: " + str(artGenInstance.paramY) + ", Z: " + str(artGenInstance.paramZ) + ", Path: " + str(artGenInstance.pathToOutputData) + "\n");

    artGenInstance.startArtGeneration();
    
    # Right now a delay goes through a timer object, which can then be used to call a callback to exit out of TD.
    #  Ideally it would be nice to use a class method to handle the stopping of recording cleanly, and then exiting.
    #  THe current implementation works for now.
    artGenInstance.startGenerationDelay();


    # exit();


def stop():
    global artGenInstance
    artGenInstance.stopArtGeneration();
    exit();

artGenInstance = AGD_ArtGenerator();
    
sys.stdout.write("\n\n***Starting New Instance***\n");

sys.stdout.write("Launch Gen\n")

run();