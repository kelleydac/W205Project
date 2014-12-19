#! /usr/bin/env python
# created 26 Nov 2014 DK for W205 final project

from mrjob.job import MRJob
import sys, os
from os.path import join, isfile
import numpy
import h5py

# define this as global -- doesn't seem to work as instance variable
target = {}
#targetPath = '/Users/doug/Documents/MIDS/W205/FinalProject/EMR'
targetPath = '.'
if not 'pr' in target:
    fd=open(join(targetPath,'prTarget.txt'),'r');
    target['pr'] = numpy.fromfile(fd, count=12, sep='\n');
    fd.close();

if not 'tasmin' in target:
    fd=open(join(targetPath, 'tasminTarget.txt'),'r');
    target['tasmin'] = numpy.fromfile(fd, count=12, sep='\n');
    fd.close();

if not 'tasmax' in target:
    fd=open(join(targetPath, 'tasmaxTarget.txt'),'r');
    target['tasmax'] = numpy.fromfile(fd, count=12, sep='\n');
    fd.close();

class Where2Move(MRJob):

    def configure_options(self):
        super(Where2Move, self).configure_options()

    def correlateTarget(self, _, tag):
        fileTags=tag.rsplit('/');
        scen = fileTags[0]
        var = fileTags[1]
        year = int(fileTags[2])
        latIndex = int(fileTags[3])
        lonIndex = int(fileTags[4])
        yearEnd = ((year//5)+1)*5
        yearStart = yearEnd - 4
        yearIndex = (year - yearStart)*12
        fRoot = '/mnt/s3/NEX-quartile/'
        flink1 = '/mon/atmos/'
        flink2 = '/r1i1p1/v1.0/CONUS'
        filePath = fRoot + scen + flink1 + var + flink2
        filePath = '/Users/doug/Documents/MIDS/W205/FinalProject/EMR'
        fileName = var + '_ens-avg_amon_' + scen + '_CONUS_' + str(yearStart) + '01-' + str(yearEnd) + '12.nc'
        #print 'Trying ' + join(filePath, fileName) + ' ' + str(isfile(join(filePath, fileName)))
        try:
            fd = h5py.File(join(filePath, fileName), 'r');
            #print tag
            nlats = fd['lat'].size
            nlons = fd['lon'].size
            if latIndex in range(0, nlats):
                if lonIndex in range(0, nlons):
                    sig = fd[var][yearIndex:yearIndex+12,latIndex,lonIndex]
                    corr = sum(sig*target[var])/numpy.sqrt(sum(sig)*sum(target[var]))
                    corr /= sum(target[var])/12.0
                    outputValue = str(corr)
                    yield tag, outputValue
        except IOError:
            pass

# still need to consolidate outputs for a given location

    def steps(self):
        return [self.mr(mapper=self.correlateTarget)]

if __name__ == '__main__':
   mr_job = Where2Move()
   with mr_job.make_runner() as runner:
       runner.run()
       for line in runner.stream_output():
           key, value = mr_job.parse_output_line(line)
           print key,value