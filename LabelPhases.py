import csv
import numpy as np
import os
import re
from sklearn.model_selection import train_test_split

def dataRead (read,write):
    with open(read) as datafile:
        data = csv.reader(datafile,delimiter = ',')
        for row in data:
            for x in range(len(row)):
                write[x].append(float(row[x]))
    return (write)

def dataWrite (datafile,datalist):
    with open(datafile, 'wb') as csvfile:
        write = csv.writer(csvfile, delimiter = ',')
        for _ in datalist:
            write.writerow(_)

def labelPhases (ID,t1,t2,t3,dataset):
    #find index that matches timestamp of beginning of phase 1
    dataset = np.array(dataset).T.tolist()
    t = int(0)
    while dataset[t][0] <= t1:
        t += 1
    dataset = dataset[t:]
    for _ in range(len(dataset)):
        if all([dataset[_][0] >= t1, dataset[_][0] < t2]):
            dataset[_].insert(4,int(1))
        elif all([dataset[_][0] >= t2, dataset[_][0] < t3]):
            dataset[_].insert(4,int(2))
        elif dataset[_][0] >= t3:
            dataset[_].insert(4,int(3))
        dataset[_].insert(5,ID)
    return dataset

def readAllForTrial(acl,acr,gyl,gyr):
    lefta = [[],[],[],[]]
    righta = [[],[],[],[]]
    leftg = [[],[],[],[]]
    rightg = [[],[],[],[]]

    lefta = dataRead(acl,lefta)
    righta = dataRead(acr,righta)
    leftg = dataRead(gyl,leftg)
    rightg = dataRead(gyr,rightg)
    return(lefta, righta, leftg, rightg)

def processByFile(gID,sID,tID,leftacc,rightacc,leftgyro,rightgyro):
    print leftacc

    l_a,r_a,l_g,r_g = readAllForTrial(leftacc,rightacc,leftgyro,rightgyro)

    # Create threshold for pick up blade
    threshold = np.mean(abs(np.asarray((l_a[3][:25]))))*1

    # Compare z-movement against threshold, set = "start"
    index = 0
    while abs(l_a[3][index]) < threshold:
        index += 1
    p1t = l_a[0][index]
    p1i = index
    print p1i
    print threshold
    print p1t

    # Find location where motion begins to go steady again
    while abs(max(l_a[3][index:index+100]) - min(l_a[3][index:index+100])) > 0.15:
        index += 1
    p2t = l_a[0][index]
    p2i = index

    # Create threshold for take blade out, compare against threshold
    threshold = abs(max(l_a[3][index:index+50]))
    while abs(l_a[3][index]) < threshold:
        index += 1
        '''
        print index
        print l_a[3][index]
        print threshold
        '''
    p3t = l_a[0][index]
    p3i = index

    l_a = labelPhases(gID,p1t,p2t,p3t,l_a)
    # r_a = labelPhases(gID,p1t,p2t,p3t,r_a)
    l_g = labelPhases(gID,p1t,p2t,p3t,l_g)
    # r_g = labelPhases(gID,p1t,p2t,p3t,r_g)

    # l_a = labelPhases(gID,0,0,0,l_a)
    # r_a = labelPhases(gID,0,0,0,r_a)
    # l_g = labelPhases(gID,0,0,0,l_g)
    # r_g = labelPhases(gID,0,0,0,r_g)

    dataWrite(str(sID) + "-" + str(tID) + "acc-left-labeled.csv",l_a)
    dataWrite(str(sID) + "-" + str(tID) + "gyro-left-labeled.csv",l_g)
    dataWrite(str(sID) + "-" + str(tID) + "acc-right-labeled.csv",r_a)
    dataWrite(str(sID) + "-" + str(tID) + "gyro-right-labeled.csv",r_g)


'''
'''

train_data = []
filelist = []
test_data = []

with open('training_set.csv') as trainfile:
    data = csv.reader(trainfile,delimiter=',')
    for _ in data:
        train_data.append(str(_))

with open('test_set.csv') as testfile:
    data = csv.reader(testfile,delimiter=',')
    for _ in data:
        test_data.append(str(_))

with open('file_set.csv') as filedata:
    data = csv.reader(filedata,delimiter=',')
    for _ in data:
        filelist.append(str(_))

for _ in train_data:
    trialID = _[-12:-11]
    AR = str()
    AL = str()
    GR = str()
    GL = str()
    if (re.search(r'CA1',_)):
        groupID = 0
        subjID = "./CA1-2016/" + str(_[13:15]) + "/"
    elif(re.search(r'Attendings',_)):
        groupID = 1
        subjID = "./Attendings/" + str(_[15:17]) + "/"
    for f in filelist:
        f = f[2:-2]
        regex = re.escape(subjID) + r'[\-\_\/0-9A-Za-z]*' + re.escape(trialID) + r"\-(left|right)\.csv$"
        # re.escape(subjID) + r'[\-\_\/0-9A-Za-z]*' + re.escape(trialID) + r"\-left\.csv$"
        if (re.search(regex,f) != None):
            if (re.search(r'Acc', f) != None):
                if (re.search(r'left', f) != None):
                    AL = f
                else:
                    AR = f
            elif (re.search(r'Gyro',f) != None):
                if (re.search(r'left', f) != None):
                    GL = f
                else:
                    GR = f

    processByFile(groupID,subjID,trialID,AL,AR,GL,GR)

    #feed file info into readallfortrial
    #process each file w processbyfile

for _ in test_data:
    trialID = _[-12:-11]
    AR = str()
    AL = str()
    GR = str()
    GL = str()
    if (re.search(r'CA1',_)):
        groupID = 0
        subjID = "./CA1-2016/" + str(_[13:15]) + "/"
    elif(re.search(r'Attendings',_)):
        groupID = 1
        subjID = "./Attendings/" + str(_[15:17]) + "/"
    for f in filelist:
        f = f[2:-2]
        regex = re.escape(subjID) + r'[\-\_\/0-9A-Za-z]*' + re.escape(trialID) + r"\-(left|right)\.csv$"
        if (re.search(regex,f) != None):
            if (re.search(r'Acc', f) != None):
                if (re.search(r'left', f) != None):
                    AL = f
                else:
                    AR = f
            elif (re.search(r'Gyro',f) != None):
                if (re.search(r'left', f) != None):
                    GL = f
                else:
                    GR = f
    processByFile(groupID,subjID,trialID,AL,AR,GL,GR)
