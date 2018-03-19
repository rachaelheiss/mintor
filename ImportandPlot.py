from matplotlib import pyplot as mpl
import numpy as np
import csv
from glob import glob

# start of intubation -> take hands off of table
# split from phase 1 to phase 2 -> hold left hand steady, doing things with right
# split from phase 2 to phase 3 -> hold right hand steady, remove blade

acc1Ltime = []
acc1Lx = []
acc1Ly = []
acc1Lz = []

gyro1Ltime = []
gyro1Lx = []
gyro1Ly = []
gyro1Lz = []

gyro1Rtime = []
gyro1Rx = []
gyro1Ry = []
gyro1Rz = []

acc1Rtime = []
acc1Rx = []
acc1Ry = []
acc1Rz = []


with open('Attendings/1/Sim/Acc-1-left.csv') as datafile:
    data = csv.reader(datafile,delimiter = ',')
    for row in data:
        acc1Ltime.append(float(row[0]))
        acc1Lx.append(float(row[1]))
        acc1Ly.append(float(row[2]))
        acc1Lz.append(float(row[3]))

with open('Attendings/1/Sim/Acc-1-right.csv') as datafile:
    data = csv.reader(datafile,delimiter = ',')
    for row in data:
        acc1Rtime.append(float(row[0]))
        acc1Rx.append(float(row[1]))
        acc1Ry.append(float(row[2]))
        acc1Rz.append(float(row[3]))

with open('Attendings/1/Sim/Gyro-1-left.csv') as datafile:
    data = csv.reader(datafile,delimiter = ',')
    for row in data:
        gyro1Ltime.append(float(row[0]))
        gyro1Lx.append(float(row[1]))
        gyro1Ly.append(float(row[2]))
        gyro1Lz.append(float(row[3]))

with open('Attendings/1/Sim/Gyro-1-right.csv') as datafile:
    data = csv.reader(datafile,delimiter = ',')
    for row in data:
        gyro1Rtime.append(float(row[0]))
        gyro1Rx.append(float(row[1]))
        gyro1Ry.append(float(row[2]))
        gyro1Rz.append(float(row[3]))

mpl.figure(1)

mpl.subplot(211)
mpl.plot(acc1Lx, label = 'X')
mpl.plot(acc1Ly, label = 'Y')
mpl.plot(acc1Lz, label = 'Z')
mpl.title('Attending Accelerations')
mpl.xlabel('Time Index')
mpl.ylabel('Left Acceleration')
mpl.legend()

mpl.subplot(212)
mpl.plot(acc1Rx, label = 'X')
mpl.plot(acc1Ry, label = 'Y')
mpl.plot(acc1Rz, label = 'Z')
mpl.xlabel('Time Index')
mpl.ylabel('Right Acceleration')

mpl.figure(2)

mpl.subplot(211)
mpl.plot(gyro1Ltime, gyro1Lx, label = 'Left X')
mpl.plot(gyro1Ltime, gyro1Ly, label = 'Left Y')
mpl.plot(gyro1Ltime, gyro1Lz, label = 'Left Z')
mpl.xlabel('Time')
mpl.ylabel('Left Rotation')
mpl.legend()

mpl.subplot(212)
mpl.plot(gyro1Rtime, gyro1Rx, label = 'Right X')
mpl.plot(gyro1Rtime, gyro1Ry, label = 'Right Y')
mpl.plot(gyro1Rtime, gyro1Rz, label = 'Right Z')
mpl.xlabel('Time')
mpl.ylabel('Right Rotation')

mpl.show()

median = max(sorted(acc1Lz[:100]))
threshold = median*1.1

index = 0
while acc1Lz[index] < threshold:
    index += 1

print index, acc1Lz[index]
print acc1Ltime[index]
