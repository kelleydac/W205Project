#! /usr/bin/env python27
#
# created as standalone mapper for W205 project 4 Dec 2014 DK
import sys, os
from os.path import join, isfile
import numpy
import h5py
import time

for line in sys.stdin:
    try:
        target
    except NameError:
        target = {}
        #targetPath = '/Users/doug/Documents/MIDS/W205/FinalProject/EMR'
        targetPath = '/home/hadoop'
        if not 'pr' in target:
            try:
                fd=open(join(targetPath,'prTarget.txt'),'r');
            except IOError:
                # try again after waiting 30 seconds
                time.sleep(30)
                fd = open(join(targetPath, 'prTarget.tx'), 'r');
            target['pr'] = numpy.fromfile(fd, count=12, sep='\n');
            sys.stderr.write('prTarget loaded\n');
            fd.close();

        if not 'tasmin' in target:
            try:
                fd=open(join(targetPath, 'tasminTarget.txt'),'r');
            except IOError:
                # try again after waiting 30 seconds
                time.sleep(30);
                fd=open(join(targetPath, 'tasminTarget.txt'),'r');
            target['tasmin'] = numpy.fromfile(fd, count=12, sep='\n');
            sys.stderr.write('tasminTarget loaded\n');
            fd.close();

        if not 'tasmax' in target:
            try:
                fd=open(join(targetPath, 'tasmaxTarget.txt'),'r');
            except IOError:
                # try again after waiting 30 seconds
                time.sleep(30);
                fd=open(join(targetPath, 'tasmaxTarget.txt'),'r');
            target['tasmax'] = numpy.fromfile(fd, count=12, sep='\n');
            sys.stderr.write('tasmaxTarget loaded\n');
            fd.close();

    sys.stderr.write("Processing " + line)
    fileTags=line.split('/');
    scen = fileTags[0]
    var = fileTags[1]
    year = int(fileTags[2])
    latIndex = int(fileTags[3])
    lonIndex = int(fileTags[4])
    if year % 5:
        #round it up
        yearEnd = ((year//5)+1)*5
    else:
        yearEnd = year
    yearStart = yearEnd - 4
    yearIndex = (year - yearStart)*12
    fRoot = '/mnt/s3/NEX-quartile/'
    flink1 = '/mon/atmos/'
    flink2 = '/r1i1p1/v1.0/CONUS'
    filePath = fRoot + scen + flink1 + var + flink2
    #filePath = '/Users/doug/Documents/MIDS/W205/FinalProject/EMR'
    fileName = var + '_ens-avg_amon_' + scen + '_CONUS_' + str(yearStart) + '01-' + str(yearEnd) + '12.nc'
    sys.stderr.write('Trying ' + join(filePath, fileName) + ' ' + str(isfile(join(filePath, fileName))) + '\n')
    try:
        fd = h5py.File(join(filePath, fileName), 'r');
        sys.stderr.write('Opened ' + fileName + '\n')
        nlats = fd['lat'].size
        nlons = fd['lon'].size
        if latIndex in range(0, nlats):
            if lonIndex in range(0, nlons):
                sig = fd[var][yearIndex:yearIndex+12,latIndex,lonIndex]
                if numpy.amax(sig) < 1e20:
                    corr = sum(sig*target[var])/numpy.sqrt(sum(sig)*sum(target[var]))
                    corr /= sum(target[var])/12.0
                    outputValue = str(corr)
                    sys.stderr.write('Score: ' + outputValue + '\n')
                    print line.rstrip('\n') + ' ' + outputValue
                else:
                    sys.stderr.write(str(latIndex) + ', ' + str(lonIndex) + ' data invalid\n');
        # medium clusters can handle 2 files open without this
        fd.close()
    except IOError:
        sys.stderr.write('Could not open ' + join(filePath, fileName) + '\n')
        pass