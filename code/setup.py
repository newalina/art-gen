from setuptools import setup, find_packages


# Instructions on Setting-Up Python 
# 1) Ensure requirements.txt is met
# 2) Ensure the Python Interpretter being used is that of the machine and or venv's Python
# 3) run 'pip install .' in art-gen/code. This creates and installs the modules to your Python path
# 4) test changes.
# 5) If updates need to be done to the module, run 'pip uninstall art-gen' and redo steps 3-4

setup(
    name="art-gen",
    version="1.0",
    packages=find_packages()
)