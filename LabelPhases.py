import csv
import numpy as np
import os
import re
from sklearn.model_selection import train_test_split

def data_read (read,write):
    with open(read) as datafile:
        data = csv.reader(datafile,delimiter = ',')
        for row in data:
            for x in range(len(row)):
                write[x].append(float(row[x]))
    return (write)

def data_write (datafile,datalist):
    with open(datafile, 'wb') as csvfile:
        write = csv.writer(csvfile, delimiter = ',')
        for _ in datalist:
            write.writerow([_])

def label_phases (t1,t2,t3,dataset):
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
        elif all([dataset[_][0] >= t2, dataset[_][0] < t3]):
            dataset[_].insert(4,int(3))
    return dataset

filelist = []
splitlist = []

#find only .csv files and exclude problem data and first trials
path = "./"
extension = ".csv"
for root, dirs, files in os.walk(path):
    for name in files:
        if os.path.splitext(name)[-1] == extension:
            if (re.search(r'Problem Data',root) == None) and (re.search(r'Slow',root) == None) and (re.search(r'[-_\w]+1-left.csv$',name) == None) and (re.search(r'[-_\w]+1-right.csv$', name) == None):
                filelist.append(os.path.join(root,name))
                if re.search(r'^Acc[-_\w]+left\.csv$',name):
                    splitlist.append(os.path.join(root,name))

# Proportion of trials for test
test_proportion = .3

train_list,test_list = train_test_split(splitlist,test_size = test_proportion)
print ('Training length: ' + str(len(train_list)))
print ('Test length: ' + str(len(test_list)))
print ('Total length: ' + str(len(splitlist)))

# Write to .csv file: training data and test data
data_write('training_set.csv', train_list)
data_write('test_set.csv', test_list)

accL = [[], [], [], []]
gyroL = [[], [], [], []]
gyroR = [[], [], [], []]
accR = [[], [], [], []]

accL = data_read('Attendings/1/Sim/Acc-1-left.csv',accL)
accR = data_read('Attendings/1/Sim/Acc-1-right.csv',accR)
gyroL = data_read('Attendings/1/Sim/Gyro-1-left.csv',gyroL)
gyroR = data_read('Attendings/1/Sim/Gyro-1-right.csv',gyroR)

# Create threshold for pick up blade
threshold = (max(accL[3][:50]))*1.1

# Compare z-movement against threshold, set = "start"
index = 0
while accL[3][index] < threshold:
    index += 1
p1t = accL[0][index]
p1i = index

# Find location where motion begins to go steady again
while abs(max(accL[3][index:index+25]) - min(accL[3][index:index+25])) > 0.1:
    index += 1
p2t = accL[0][index]
p2i = index

# Create threshold for take blade out, compare against threshold
threshold = max(accL[3][index:index+25])*1.1
while accL[3][index] < threshold:
    index += 1
p3t = accL[0][index]
p3i = index

accL = label_phases(p1t,p2t,p3t,accL)
accR = label_phases(p1t,p2t,p3t,accR)
gyroL = label_phases(p1t,p2t,p3t,gyroL)
gyroR = label_phases(p1t,p2t,p3t,gyroR)

print('AccL: ' + str(accL[0:2]))
print('GyroL: ' + str(gyroL[0:2]))
