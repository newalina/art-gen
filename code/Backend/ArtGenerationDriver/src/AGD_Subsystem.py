# Project Modules
from AGD_ArtGenerator import AGD_ArtGenerator
from AGD_Definitions import AGD_Definitions as AGD_DEF;
import threading
from collections import deque
import logging
import os

# Object 0
testArtGenerator = AGD_ArtGenerator(0, 125, 32, 51);
testArtGenerator.writeToJSON();
testArtGenerator.startTouchDesigner();
# Here do something with the data...
print("Succesfully Quit Program");

# Object 1
test2 = AGD_ArtGenerator(0, 1, 24, 61);
test2.writeToJSON();
test2.startTouchDesigner();
# Here do something with the data...
print("Succesfully Quit Program");

# Need a way to clean up too many files being stored in data folder (Should only maintain 64-128 most recent files?)
# Need to determine what to do with data output once the system has it in a file. Do we want this in JSON, Base-64, idk
# Need to determine if current exit strategy is OK, or if we want a more SW heavy approach using personally declared files.
#   This does not need to be OOP. Could use helper functions to determine if too much data in folder, program is stopped recording,
#   etc before closing out the program .
# Is there a way to add paths for TD either in TD or by some helper function that is called to add to sys path prior to each individula
#   function requiring AGD code?
# Is there a way to automate / load in personal files without having to hardcode in the directory? Can an expression be used using the ROOT_DIR, etc
#   to dynamically select where the file is so the program can be console independent? Can all of this happen at runtime?
# NOTE: The answer two the two previous questions may lie within an initialization .py file that is run everytime TD boots up so that it properly sets
#   all of the required information needed for it while running without forcing the TD Designer / Py Developer to hardcode everything. We will have to
#   adhere to a strict naming policy if this is our path forward.

# We should probably update our documentation for code style and create documentation for naming policies to adhere to in Touch Designer so the Py Developers
#   and TD Designers are on the same page regarding their implementations. 
# Standardize everything. 


class AGD_Subsystem:

    def __init__(self):
        # expects a list of [modelSelection, param1, param2, param3]
        self.generationQueue = deque();
        self.generatedOutput = deque();

        # init a thread to handle the generation queue
        self.generationThread = threading.Thread(target=self.processGenerationQueue);

    def appendGenerationRequest(self, object) -> int:

        if( len(self.generationQueue) >= AGD_DEF.MAX_QUEUE_SIZE.value ):
            print("ERROR: Unable to append to queue");
            return -1;
        else:
            self.generationQueue.append(object);
        
        return 0;

    def popGenerationRequest(self):
        logging.debug("Popping Generation Request");
        return self.generationQueue.popleft();

    def checkIfFileExists(self, path):
        return os.path.isfile(path);

    def processGenerationQueue(self):
        while(True):
            if( len(self.generationQueue) > 0 ):

                a, param1, param2, param3 = self.popGenerationRequest();
                artGenerator = AGD_ArtGenerator(a, param1, param2, param3);
                artGenerator.writeToJSON();
                artGenerator.startTouchDesigner();

                # check if the file exists
                while( not self.checkIfFileExists(artGenerator.pathToOutputData) ):
                    pass;

                self.generatedOutput.append(artGenerator);                

    

# DO ERROR CHECKING AND LOGGING EVERYHWERE THAT IS HUMANELY POSSIBLE. SET UP SYSTEM TO ALWAYS RETURN ERROR CODES AFTER EXECUTION!!!!!!

# Ok, so the thought here is to create a main program that initializes everything that is used (The flask app, AGD, Databases, everything). Within this file / main program,
#  we will continually analyze a queue that contains a series of AGD_ArtGenerator elements. On reception of data from the website, we create a new object in the HTML interface.
#  we then append this to the subsystem queue which was initialized in the main program. This queue is then analyzed to take the current front of queue for processing. When processing
#  is complete in touch designer, there must be a signal sent from the TD application out to the main driver application to say object "X" has completed, which will remove it fromm the
#  front of the queue, and will enable the next element to begin processing the next time the main loop iterates. 


# It seems that once we open touch designer, it will block all other processing. It may be good to throw this in its own thread that handles the generation. This removes the need to handle any
#  signals sent back to teh system since we know that if td closes, it has finished processing and if it finishes processing, that we can dequeue the current object, and start processing on the next object
#


# Once we exit, we read the file thats been written and handle the data accordingly.


# Probably need a centralized place to hold variables

# Think through what can be edited / what should be static. What is really the best way to implement this. 

# May need to create a virtual environemnt relative to the project path that can be used so Touch Designer can work on any machine.
#  Currently I am hardcoding values for my laptop in terms of python libraries, python files, etc. 
# Use this for importing modules: https://nvoid.gitbooks.io/introduction-to-touchdesigner/content/Python/9-6-External-Modules.html