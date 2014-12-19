#! /usr/bin/env python
# Generate tags for points to read for W205 project
import sys
from numpy import sqrt

# loop over scenarios
# get a year
# get a source
# get a radius

def main():
    if len(sys.argv) != 6:
    	print "Usage: python genTags year sourceLat sourceLon radius step"
    	return;
    
    year = int(sys.argv[1])
    
    ssLat = int(sys.argv[2])
    
    ssLon = int(sys.argv[3])
    
    radius = int(sys.argv[4])
    
    step = int(sys.argv[5])
    
    for x in range(0, 3105, step):
        for y in range(0, 7025, step):
            x1 = x - ssLat;
            y1 = y - ssLon;
            if sqrt(x1*x1 + y1*y1) < float(radius):
            	print 'rcp26/pr/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp26/tasmax/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp26/tasmin/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp45/pr/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp45/tasmax/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp45/tasmin/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp60/pr/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp60/tasmax/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp60/tasmin/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp85/pr/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp85/tasmax/'+str(year)+'/'+str(x)+'/'+str(y)
            	print 'rcp85/tasmin/'+str(year)+'/'+str(x)+'/'+str(y)

if __name__ == '__main__':
	main()
