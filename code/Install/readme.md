# Install Directory
This directory contains all of the files necessary to properly install any required functionality of the Art Generator Project. <b/>


## Backend
### Requirements
Install the requirements file as normal using 'pip install -r requirements'

### Setup
To initialize the project path's properly, run 'pip install .' in the Install directory. This will install all of the code as a package. If updates to this code are made, then the developer will have to run 'pip uninstall art-gen' before re-installing using 'pip install .'. There may be a better way to do this, but for now this works. <b/>
Additional directories will be made as a result of this install and that is OK as long as we do not promote them to our repository. As of now, they are setup to be ignored. Additionally, I think you can just delete the egg-info directory with no consequence. 


Instructions on Setting-Up Python 
1) Ensure requirements.txt is met
2) Ensure the Python Interpretter being used is that of the machine and or venv's Python
3) run 'pip install .' in art-gen/code/Install. This creates and installs the modules to your Python path
4) test changes.
5) If updates need to be done to the module, run 'pip uninstall art-gen' and redo steps 3-4