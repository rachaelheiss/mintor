'''
MINTOR
TraverseandSplit.py
J. Card, R. Heiss, M. Mora Sanchez, B. Tou
Northeastern University MIE Capstone Spring 2018

This traverses the directories in the project path, removes files that we do
not want to add to our file directory, and will split the data into a training
set and a testing set.
'''

# Necessary libraries for this script include os (to traverse the project
# directory), csv (to read and write .csv files), re (to match regular
# expressions), and train_test_split from the sklearn library (randomly
# splits an input array by inputted percentages)
import os
import csv
import re
from sklearn.model_selection import train_test_split

# Inputs:   datafile    string that contains file name for a .csv where
#                       information should be output
#           datalist    list containing paths to datafiles to be used later.
#                       Entries in this list will be written out as a row in
#                       datafile

# Output:   none
# Function takes the input list and writes each entry in the list out as a row
# in a csv. The path to the csv is the input datafile.
def data_write (datafile,datalist):
    # Open the file where the data will be written
    with open(datafile, 'wb') as csvfile:
        # Call a writer function and define the delimeter to be ","
        write = csv.writer(csvfile, delimiter = ',')
        # Iterate through each entry in the list to be written
        for _ in datalist:
            # Write the entry out as a row in the datafile.
            write.writerow([_])


# Create two empty arrays where the filenames of interest will be appended
filelist = []
splitlist = []

# Set path to top of directory, and set the extension to only include .csv files
path = "./"
# This path includes 2015 and 2016 data
extension = ".csv"

# Loop through the all files in the path (top of directory)
for root, dirs, files in os.walk(path):
    # For each file in the directory
    for name in files:
        # If the split name (<file><extension>) == .csv
        if (os.path.splitext(name)[-1] == extension):
            # If the filename doesn't incliude "set.csv", "average", "Problem Data", "Slow", "left-1", or "right-1", and does include "Sim"
            if (re.search(r'set\.csv',name) == None) and (re.search(r'Sim',root)) and (re.search(r'average', name) == None) and (re.search(r'Problem Data',root) == None) and (re.search(r'Slow',root) == None) and (re.search(r'[-_\w]+1-left.csv$',name) == None) and (re.search(r'[-_\w]+1-right.csv$', name) == None):
                # Add the path to that file to the "filelist" list
                filelist.append(os.path.join(root,name))
                # If the file includes left accelerometer data (the identifier used for a trial)
                if re.search(r'^Acc[-_\w]+left\.csv$',name):
                    # Add the trial to a the "splitlist" list
                    splitlist.append(os.path.join(root,name))

# Proportion of trials for testing group is set below.
test_proportion = .3
# train_list and test_list will will be created using the
# train_test_split function with the proportion indicated above
train_list,test_list = train_test_split(splitlist,test_size = test_proportion)

# The number of training trials, number of testing trials, and total trials
# are printed out.
print ('Training length: ' + str(len(train_list)))
print ('Test length: ' + str(len(test_list)))
print ('Total length: ' + str(len(splitlist)))

# Write to .csv file: training data and test data
data_write('training_set.csv', train_list)
data_write('test_set.csv', test_list)
data_write('file_set.csv', filelist)
