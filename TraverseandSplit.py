import os
import csv
import re
from sklearn.model_selection import train_test_split

def data_write (datafile,datalist):
    with open(datafile, 'wb') as csvfile:
        write = csv.writer(csvfile, delimiter = ',')
        for _ in datalist:
            write.writerow([_])

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

# Proportion of trials for testing group
test_proportion = .3
train_list,test_list = train_test_split(splitlist,test_size = test_proportion)
print ('Training length: ' + str(len(train_list)))
print ('Test length: ' + str(len(test_list)))
print ('Total length: ' + str(len(splitlist)))

# Write to .csv file: training data and test data
data_write('training_set.csv', train_list)
data_write('test_set.csv', test_list)
