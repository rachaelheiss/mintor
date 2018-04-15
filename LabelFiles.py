'''
MINTOR
LabelFiles.py
J. Card, R. Heiss, M. Mora Sanchez, B. Tou
Northeastern University MIE Capstone Spring 2018

This script reads in all of the datafiles we are interested in processing,
groups them by trial, labels them with their respective group ID (1 for
novice, 2 for expert), and re-writes them to labeled .csv files by sensor
and hand. These labeled .csv files are what feed into the models.

Included in this script are also functions that would label group ID and in the
next column label phases throughout the trial.  This functionality is not
reliable in its current state but is included for later development.
'''

# The necessary libraries to run this script include csv (to read and writer
# .csv files), numpy (for mathematical operations standard Python doesn't
# support), and re (to match regular expressions)
import csv
import numpy as np
import re

# Inputs:   filename    string path to the .csv file to be read into an array
#           write       empty list data from the .csv will be written to

# Output:   write       list containing the contents of filename
# Function reads in a .csv file whose path is noted by filename. The contents
# of filename are saved in a list called write, which is empty upon being called.
# Write is returned as a list with the information from th file.
def dataRead (filename,write):
    # Open the file, and internally refer to it as "datafile"
    with open(filename) as datafile:
        # Read in the .csv contents into "data"
        data = csv.reader(datafile,delimiter = ',')
        # For each row, in the contents of "data"
        for row in data:
            # For each segment of the row
            for x in range(len(row)):
                # Add the segment to the end of "write"
                write[x].append(float(row[x]))
    # Return the list with all of the data in it.
    return write

# Inputs:   datafile    string that contains file name for a .csv where
#                       information should be output
#           datalist    list containing paths to datafiles to be used later.
#                       Entries in this list will be written out as a row in
#                       datafile

# Output:   none
# Function takes the input list and writes each entry in the list out as a row
# in a csv. The path to the csv is the input datafile.
def dataWrite (datafile,datalist):
    # Open the file where the data will be written
    with open(datafile, 'wb') as csvfile:
        # Call a writer function and define the delimeter to be ","
        write = csv.writer(csvfile, delimiter = ',')
        # Iterate through each entry in the list to be written
        for _ in datalist:
            # Write the entry out as a row in the datafile.
            write.writerow(_)

# Inputs:   ID          integer where 1 represents novice, 2 represents expert
#           dataset     list containing sensor output. contains 4 lists of n
#                       records

# Output:   dataset     list containing sensor output labeled by group id in
#                       each row. n lists of 5 records.
# Function takes the input groupID and list and transposes the list. It then
# adds the groupID in the 5th column of each row.
def labelGroupID (ID,dataset):
    # Transpose the data within the list because it has been read in as four
    # lists containing n records within each. Instead we would like n lists
    # with 4 records [time, x, y, z]. We will insert the groupID in column 5
    dataset = np.array(dataset).T.tolist()
    # For each row for the length of the list of data
    for _ in range(len(dataset)):
        # Insert the groupID for that dataset in the fifth position.
        # Each row now contains [time, x, y, z, group]
        dataset[_].insert(4,ID)
    # Return the new dataset
    return dataset

# Inputs:   acl         string filepath to left accelerometer data for one trial
#           acr         string filepath to right accelerometer data for same trial
#           gyl         string filepath to left gyroscope data for same trial
#           gyr         string filepath to right gyroscope data for same trial

# Outputs:  lefta       nested list of 4 lists containing left acc data
#           righta      nested list of 4 lists containing right acc data
#           leftg       nested list of 4 lists containing left gyro data
#           rightg      nested list of 4 lists containing right gyro data
# Function takes 4 input filepaths for one trial's worth of data, and reads the
# data into 4 nested lists of 4 lists so all data for that trial is available.
def readAllForTrial(acl,acr,gyl,gyr):
    # Create 4 empty nested lists of 4 lists to store the data
    lefta = [[],[],[],[]]
    righta = [[],[],[],[]]
    leftg = [[],[],[],[]]
    rightg = [[],[],[],[]]

    # Use established dataread function to read the filepaths' data into the
    # empty lists created above.
    lefta = dataRead(acl,lefta)
    righta = dataRead(acr,righta)
    leftg = dataRead(gyl,leftg)
    rightg = dataRead(gyr,rightg)
    # Return all four nested lists for the trial.
    return(lefta, righta, leftg, rightg)

# Inputs:   gID         int group ID -- either 1 for novice or 2 for expert
#           sID         string subject ID -- beginning of filepath for the trial
#                       being processed. (Ex: "./CA1-2016/30/")
#           tID         string containing 1 digit long trial ID. Taken from
#                       filepath for the trial being processed.
#           leftacc     string containing filepath to left-hand accelerometer
#                       for the trial.
#           rightacc    string containing filepath to right-hand accelerometer
#                       for the trial.
#           leftgyro    string containing filepath to left-hand gyroscope
#                       for the trial.
#           rightgyro   string containing filepath to right-hand gyroscope
#                       for the trial.

# Output:   none
# Function reads in the data from each file into 4 nested lists using the
# readAllForTrial function above. Then it adds a column to each with the
# subject's groupID using the labelGroupID function above. Finally, it writes
# out these new nested lists into .csv files using the dataWrite function above.
def processByFile(gID,sID,tID,leftacc,rightacc,leftgyro,rightgyro):
    # Read the information at the four filepaths into four nested lists.
    l_a,r_a,l_g,r_g = readAllForTrial(leftacc,rightacc,leftgyro,rightgyro)

    # Transpose this data, and add the group ID in each record.
    l_a = labelGroupID(gID,l_a)
    r_a = labelGroupID(gID,r_a)
    l_g = labelGroupID(gID,l_g)
    r_g = labelGroupID(gID,r_g)

    # Write out these new nested lists into new files grouped by sensor and
    # hand. This makes it easier to process the information in the models
    # created in MATLAB.
    dataWrite("./LeftAcc/" + str(subjID[-3:-1])+ "-" + str(tID) + "-acc-left-labeled.csv",l_a)
    dataWrite("./LeftGyro/" + str(subjID[-3:-1])+ "-" + str(tID) + "-gyro-left-labeled.csv",l_g)
    dataWrite("./RightAcc/" + str(subjID[-3:-1])+ "-" + str(tID) + "-acc-right-labeled.csv",r_a)
    dataWrite("./RightGyro/" + str(subjID[-3:-1])+ "-" + str(tID) + "-gyro-right-labeled.csv",r_g)

'''
The following two functions are not used in the file as it exists, but are
included for further development. The processByPhaseandFile function has been
repeatedly modified to try to find an appropriate mathematical method for
locating inactivity, and a threshold for that inactivity.
'''

# Inputs:   ID          integer where 1 represents novice, 2 represents expert
#           t1          float containing the timestamp for beginning of phase 1
#           t2          float containing the timestamp for beginning of phase 2
#           t3          float containing the timestamp for beginning of phase 3
#           dataset     list containing sensor output. contains 4 lists of n
#                       records

# Output:   dataset     list containing sensor output labeled by group id in
#                       each row. n lists of 5 records.
# Function takes the input groupID and list and transposes the list. It then
# adds the groupID in the 5th column of each row.
def labelPhases (ID,t1,t2,t3,dataset):
    # Transpose the data within the list because it has been read in as four
    # lists containing n records within each. Instead we would like n lists
    # with 4 records [time, x, y, z]. We will insert the groupID in column 5,
    # and the phase number into column 6.
    dataset = np.array(dataset).T.tolist()
    # Initialize an incremental variable, t to 0
    t = int(0)
    # Find index that matches timestamp of beginning of phase 1
    while dataset[t][0] <= t1:
        t += 1
    # Cut off the beginning of the dataset until the index t, where phase 1
    # begins (according to threshold found in processByPhaseandFile)
    dataset = dataset[t:]
    # For every row within the dataset
    for _ in range(len(dataset)):
        # Add the groupID in the fifth column
        dataset[_].insert(4,ID)
        # If the timestamp for the row is both greater than or equal to the
        # timestamp for the beginning of phase 1 and less than the timestamp
        # for the beginning of phase 2
        if all([dataset[_][0] >= t1, dataset[_][0] < t2]):
            # Insert a "1" for phase 1 into the 6th column of the row.
            dataset[_].insert(5,int(1))
        # Else if the timestamp for the row is both greater than or equal to the
        # timestamp for the beginning of phase 2 and less than the timestamp
        # for the beginning of phase 3
        elif all([dataset[_][0] >= t2, dataset[_][0] < t3]):
            # Insert a "2" for phase 2 into the 6th column of the row.
            dataset[_].insert(5,int(2))
        # Else if the timestamp for the row is greater than or equal to the
        # timestamp for the beginning of phase 3
        elif dataset[_][0] >= t3:
            # Insert a "3" for phase 3 into the 6th column of the row.
            dataset[_].insert(5,int(3))
    # Return the same dataset, but with 5th column labeled as groupID, and
    # 6th column labeled by phase.
    return dataset

# Inputs:   gID         int group ID -- either 1 for novice or 2 for expert
#           sID         string subject ID -- beginning of filepath for the trial
#                       being processed. (Ex: "./CA1-2016/30/")
#           tID         string containing 1 digit long trial ID. Taken from
#                       filepath for the trial being processed.
#           leftacc     string containing filepath to left-hand accelerometer
#                       for the trial.
#           rightacc    string containing filepath to right-hand accelerometer
#                       for the trial.
#           leftgyro    string containing filepath to left-hand gyroscope
#                       for the trial.
#           rightgyro   string containing filepath to right-hand gyroscope
#                       for the trial.

# Output:   none
# Function reads in the data from each file into 4 nested lists using the
# readAllForTrial function above. Then it adds a column to each with the
# subject's groupID using the labelGroupID function above. Finally, it writes
# out these new nested lists into .csv files using the dataWrite function above.
def processByPhaseandFile(gID,sID,tID,leftacc,rightacc,leftgyro,rightgyro):
    # Read the information at the four filepaths into four nested lists.
    l_a,r_a,l_g,r_g = readAllForTrial(leftacc,rightacc,leftgyro,rightgyro)

    # Create threshold for pick up blade. In this case, we are looking for the
    # maximum of the first 50 records (1 second) in the z-axis of the left accel
    # times a factor of 1.25
    threshold = max(np.asarray((l_a[3][:50])))*1.25

    # Compare z-movement against threshold
    # Set an incremental index to compare z-axis movement against threshold.
    index = 0
    # While the z-movement at the index is less than the threshold continue to
    # increment the index up by one.
    while abs(l_a[3][index]) < threshold:
        index += 1
    # Once the index of the beginning of phase 1 is found for the trial, set
    # p1t equal to the timestamp at which phase 1 begins.
    p1t = l_a[0][index]
    # Just in case, save the index where phase 1 begins as p1i.
    p1i = index

    # Using the index above, find location where motion begins to go steady
    # again. The mathematical method shown looks for a location in the data
    # where the left-hand is relatively still over a period of 2 seconds or more
    # (still being defined as a maximum difference of less than 0.15 g)
    while abs(max(l_a[3][index:index+100]) - min(l_a[3][index:index+100])) > 0.15:
        index += 1
    # Once the index is found where phase 2 begins, save this timestamp in p2t
    p2t = l_a[0][index]
    # Save the index as well in p2i.
    p2i = index

    # Create threshold for take blade out, where the threshold is the maximum
    # across the period of the first second of inactivity in phase 2 times 1.25
    threshold = abs(max(l_a[3][index:index+50]))*1.25
    # While the z-axis accelerometer does not exceed this threshold, continue to
    # increment the index up by 1.
    while abs(l_a[3][index]) < threshold:
        index += 1
    # Once the index is found where phase 3 begins, save this timestamp in p3t
    p3t = l_a[0][index]
    # Save the index as well in p3i.
    p3i = index

    # Use these timestamps to label each phase in the labelPhases function.
    l_a = labelPhases(gID,p1t,p2t,p3t,l_a)
    l_g = labelPhases(gID,p1t,p2t,p3t,l_g)
    # The timstamps for right-hand do not always match up to left-hand.
    # The use of the labelPhases function for right hand is commented out
    # for now, due to this calibration problem.
    # r_a = labelPhases(gID,p1t,p2t,p3t,r_a)
    # r_g = labelPhases(gID,p1t,p2t,p3t,r_g)

    # Write out these new nested lists into new files within the subject ID
    # directory for each subject.
    dataWrite(str(sID) + "-" + str(tID) + "acc-left-labeled.csv",l_a)
    dataWrite(str(sID) + "-" + str(tID) + "gyro-left-labeled.csv",l_g)
    # The timstamps for right-hand do not always match up to left-hand.
    # The use of the dataWrite function for right hand is commented out
    # for now, due to this calibration problem.
    # dataWrite(str(sID) + "-" + str(tID) + "acc-right-labeled.csv",r_a)
    # dataWrite(str(sID) + "-" + str(tID) + "gyro-right-labeled.csv",r_g)

'''
Begin code below. Functions written above are called within this code.
'''

# Create three empty lists to save a list of file names.
train_data = []
filelist = []
test_data = []

# Open the training_set.csv created in "TraverseandSplit.py"
with open('training_set.csv') as trainfile:
    # Use the csv library reader to read the file names
    data = csv.reader(trainfile,delimiter=',')
    # For each name within the file
    for _ in data:
        # Append the file name to the train_data list.
        train_data.append(str(_))

# Open the test_set.csv created in "TraverseandSplit.py"
with open('test_set.csv') as testfile:
    # Use the csv library reader to read the file names
    data = csv.reader(testfile,delimiter=',')
    # For each name within the file
    for _ in data:
        # Append the file name to the train_data list.
        test_data.append(str(_))

# Open the file_set.csv created in "TraverseandSplit.py"
with open('file_set.csv') as filedata:
    # Use the csv library reader to read the file names
    data = csv.reader(filedata,delimiter=',')
    # For each name within the file
    for _ in data:
        # Append the file name to the filelist list.
        filelist.append(str(_))

# For each file path in the train_data list
for _ in train_data:
    # Store the trial ID (assumes one digit long)
    trialID = _[-12:-11]
    # Look for if the file is for a resident (path contains "CA1")
    if (re.search(r'CA1',_)):
        # Set groupID (novice or expert) = 1
        groupID = 1
        # Set subject ID the beginning of a file path containing the subject's
        # number (assumes two digits long, with a 4 digit year), i.e. "2015/17"
        subjID = "./CA1-" + str(_[8:15]) + "/"
    # Look for if the file is for an attending (path contains "Attendings")
    elif(re.search(r'Attendings',_)):
        # Set groupID (novice or expert) = 2
        groupID = 2
        # Set subject ID the beginning of a file path containing the subject's
        # number (assumes two digits long), i.e. "62"
        subjID = "./Attendings/" + str(_[15:17]) + "/"
    # For each filename in the list "filelist"
    for f in filelist:
        # Set the filepath equal to the path without brackets and quotes
        f = f[2:-2]
        # Set a regular expression that matches for the subject ID, some
        # combination of any numbers, any letters, hyphens, underscores, and
        # forward slashes, the trial ID, followed by either "-left.csv", or
        # "-right.csv"
        regex = re.escape(subjID) + r'[\-\_\/0-9A-Za-z]*' + re.escape(trialID) + r"\-(left|right)\.csv$"
        # Search the filename "f" to see if it matches the regular expression
        if (re.search(regex,f) != None):
            # Search the filename "f" to see if it matches "Acc"
            if (re.search(r'Acc', f) != None):
                # Search the filename "f" to see if it matches "left"
                if (re.search(r'left', f) != None):
                    # Set AL (accel left filepath) to f, or the filename
                    AL = f
                else:
                    # Set AR (accel right filepath) to f, or the filename
                    AR = f
            # Search the filename "f" to see if it matches "Gyro"
            elif (re.search(r'Gyro',f) != None):
                # Search the filename "f" to see if it matches "left"
                if (re.search(r'left', f) != None):
                    # Set GL (gyro left filepath) to f, or the filename
                    GL = f
                else:
                    # Set GR (gyro right filepath) to f, or the filename
                    GR = f
    # All AL, AR, GL, and GR are for the same trial, and will be processed as
    # part of that one trial (important for phase splitting)
    processByFile(groupID,subjID,trialID,AL,AR,GL,GR)

# For each file path in the test_data list
for _ in test_data:
    # Store the trial ID (assumes one digit long)
    trialID = _[-12:-11]
    # Look for if the file is for a resident (path contains "CA1")
    if (re.search(r'CA1',_)):
        # Set groupID (novice or expert) = 1
        groupID = 1
        # Set subject ID the beginning of a file path containing the subject's
        # number (assumes two digits long, with a 4 digit year), i.e. "2015/17"
        subjID = "./CA1-" + str(_[8:15]) + "/"
    # Look for if the file is for an attending (path contains "Attendings")
    elif(re.search(r'Attendings',_)):
        # Set groupID (novice or expert) = 2
        groupID = 2
        # Set subject ID the beginning of a file path containing the subject's
        # number (assumes two digits long), i.e. "62"
        subjID = "./Attendings/" + str(_[15:17]) + "/"
    # For each filename in the list "filelist"
    for f in filelist:
        # Set the filepath equal to the path without brackets and quotes
        f = f[2:-2]
        # Set a regular expression that matches for the subject ID, some
        # combination of any numbers, any letters, hyphens, underscores, and
        # forward slashes, the trial ID, followed by either "-left.csv", or
        # "-right.csv"
        regex = re.escape(subjID) + r'[\-\_\/0-9A-Za-z]*' + re.escape(trialID) + r"\-(left|right)\.csv$"
        # Search the filename "f" to see if it matches the regular expression
        if (re.search(regex,f) != None):
            # Search the filename "f" to see if it matches "Acc"
            if (re.search(r'Acc', f) != None):
                # Search the filename "f" to see if it matches "left"
                if (re.search(r'left', f) != None):
                    # Set AL (accel left filepath) to f, or the filename
                    AL = f
                else:
                    # Set AR (accel right filepath) to f, or the filename
                    AR = f
            # Search the filename "f" to see if it matches "Gyro"
            elif (re.search(r'Gyro',f) != None):
                # Search the filename "f" to see if it matches "left"
                if (re.search(r'left', f) != None):
                    # Set GL (gyro left filepath) to f, or the filename
                    GL = f
                else:
                    # Set GR (gyro right filepath) to f, or the filename
                    GR = f
    # All AL, AR, GL, and GR are for the same trial, and will be processed as
    # part of that one trial (important for phase splitting)
    processByFile(groupID,subjID,trialID,AL,AR,GL,GR)
