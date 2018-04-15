'''
MINTOR
Plot.py
J. Card, R. Heiss, M. Mora Sanchez, B. Tou
Northeastern University MIE Capstone Spring 2018

This script reads .csv data files for the MINTOR project. The given epoch
timestamps are translated into elapsed time. Four plots are generated to
visualize the accelerometer and gyroscope for each hand.
'''

# Necessary libraries for this file include matplotlib to plot the data
# and csv to read in the datafiles.
from matplotlib import pyplot as mpl
import csv

# Input:    timelist    list that contains timestamps in epoch time

# Output:   none
# Function modifies timelist to calculate time elapsed in seconds
# When running the function, the list is modified for use later on.
def elapsedTime (timelist):
    timelist[:] = [t - timelist[0] for t in timelist]

# Inputs:   filepath    string path to the .csv file to be read into a list
#           t           empty list for time data
#           x           empty list for acceleration in the x-direction or
#                       rotational velocity about the x-axis
#           y           empty list for acceleration in the y-direction or
#                       rotational velocity about the y-axis
#           z           empty list for acceleration in the z-direction or
#                       rotational velocity about the z-axis

# Outputs:  t           list containing time data from file
#           x           list containing acceleration (x-direction) or
#                       rotational velocity (x-axis) data from file
#           y           list containing acceleration (y-direction) or
#                       rotational velocity (y-axis) data from file
#           z           list containing acceleration (z-direction) or
#                       rotational velocity (z-axis) data from file
# Function uses csv library
# Funtion will only work for files with 4 columns where the values are
# delimited by commas (,) and with valid filename as input
# and 4 empty lists as output
def readfile (filepath, t, x, y, z):
    with open(filepath) as datafile:
        data = csv.reader(datafile,delimiter = ',')
        for row in data:
            t.append(float(row[0]))
            x.append(float(row[1]))
            y.append(float(row[2]))
            z.append(float(row[3]))
    return t, x, y, z

# Inputs:   fig         integer to use as the figure number for the plot
#           time        list of timestamps for elapsed time
#           x           list of x-axis-centric values at each timestamp in time
#           y           list of y-axis-centric values at each timestamp in time
#           z           list of z-axis-centric values at each timestamp in time
#           title       string title for the plot
#           stype       string representing sensor type where "Acc" is for
#                       accelerometer and "Gyro" is for gyroscope

# Output:  none
# Plots three axes over time with a title, legend, and fixed y-axis labels
def plotTrial (fig, time, x, y, z, title, stype):
    # Define figure number
    mpl.figure(fig)
    # Define 1x1 plot
    mpl.subplot(111)
    # Plot each axis against elapsed time
    mpl.plot(time, x, label = 'X')
    mpl.plot(time, y, label = 'Y')
    mpl.plot(time, z, label = 'Z')
    # Give plot a title (input)
    mpl.title(title)
    # Label x-axis as time with units "seconds"
    # $ allow for mathematical formatting in LaTex
    mpl.xlabel('$Time(s)$')
    # Determine sensor type, and fix y-axis labels appropriately
    if stype == 'Acc':
        mpl.ylim(-2,2)
        mpl.ylabel('$Acceleration (g)$')
    if stype == 'Gyro':
        mpl.ylim(-450,450)
        mpl.ylabel('$Rotational\; Velocity (deg/s)$')
    # Add a legend to plot
    mpl.legend()

# Create empty lists to store data read in during later functions
accLtime = []
accLx = []
accLy = []
accLz = []

gyroLtime = []
gyroLx = []
gyroLy = []
gyroLz = []

gyroRtime = []
gyroRx = []
gyroRy = []
gyroRz = []

accRtime = []
accRx = []
accRy = []
accRz = []

# Set filepath to read in for left accelerometer data
accLfile = 'CA1-2016/50/Sim/AccData_07_08_2016-09_32_56-3-left.csv'
# Use readfile function (defined above) to read in time, x, y, and z from file
accLtime, accLx, accLy, accLz = readfile(accLfile,accLtime, accLx, accLy, accLz)
# Modify left accelerometer time to be in elapsed time (s) instead of epoch time
elapsedTime(accLtime)

# Set filepath to read in for right accelerometer data
accRfile = 'CA1-2016/50/Sim/AccData_07_08_2016-09_32_51-3-right.csv'
# Use readfile function (defined above) to read in time, x, y, and z from file
accRtime, accRx, accRy, accRz = readfile(accRfile,accRtime, accRx, accRy, accRz)
# Modify right accelerometer time to be in elapsed time (s) instead of epoch time
elapsedTime(accRtime)

# Set filepath to read in for left gyroscope data
gyroLfile = 'CA1-2016/50/Sim/GyroData_07_08_2016-09_33_29-3-left.csv'
# Use readfile function (defined above) to read in time, x, y, and z from file
gyroLtime, gyroLx, gyroLy, gyroLz = readfile(gyroLfile,gyroLtime, gyroLx, gyroLy, gyroLz)
# Modify left gyroscope time to be in elapsed time (s) instead of epoch time
elapsedTime(gyroLtime)

# Set filepath to read in for right gyroscope data
gyroRfile = 'CA1-2016/50/Sim/GyroData_07_08_2016-09_33_45-3-right.csv'
# Use readfile function (defined above) to read in time, x, y, and z from file
gyroRtime, gyroRx, gyroRy, gyroRz = readfile(gyroRfile,gyroRtime, gyroRx, gyroRy, gyroRz)
# Modify right gyroscope time to be in elapsed time (s) instead of epoch time
elapsedTime(gyroRtime)

# Generate four plots, one for each data stream
plotTrial(1, accLtime, accLx, accLy, accLz, 'Accelerometer, Left Hand', 'Acc')
plotTrial(2, accRtime, accRx, accRy, accRz, 'Accelerometer, Right Hand', 'Acc')
plotTrial(3, gyroLtime, gyroLx, gyroLy, gyroLz, 'Gyroscope, Left Hand', 'Gyro')
plotTrial(4, gyroRtime, gyroRx, gyroRy, gyroRz, 'Gyroscope, Right Hand', 'Gyro')
# matplotlib method to display plots on machine
mpl.show()

# Find duration of trial (last recorded left accelerometer elapsed time)
duration = accLtime[-1]

# Print out duration
print "Duration: " + str(duration)
