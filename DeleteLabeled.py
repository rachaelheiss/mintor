'''
MINTOR
DeleteLabeled.py
J. Card, R. Heiss, M. Mora Sanchez, B. Tou
Northeastern University MIE Capstone Spring 2018

This script finds all created files after preprocessing that have "labeled"
in their file name. The script will also delete ANY file within the directory
that has this word in its name.
'''

# The required libraries are os (a library that allows traversing of folders and
# files within the defined path) and re (matches regular expressions)
import os
import re

# Set path to the top directory identified for the project.
path = "./"

# Look for all directories and files in the path (all folders and files)
for root, dirs, files in os.walk(path):
    # For each file within the folders
    for name in files:
        # If the filename includes the word "labeled" anywhere within it.
        if (re.search(r'labeled',name)):
            # Remove these files (delete them)
            os.remove(os.path.join(root,name))
