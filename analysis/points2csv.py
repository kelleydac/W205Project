#! /usr/bin/env/python
# created 14dec2014 DK convert EMR output to CSV for plotting in R
# given the results cat'd into 1 text file let's see what we have

import sys

print('point,lat,lon,year,var,scen,score')
point = 0;
for line in sys.stdin:
	key,score = line.split(' ')
	scen, var, year, latIndex, lonIndex = key.rsplit('/')
	lat = 24.0625 + float(latIndex)*0.008333333
	# use gmap convention
	lon = 234.979166 + float(lonIndex)*0.00833333 - 360.0
	print(str(point) + ',' + str(lat) + ',' + str(lon) + ',' + year + ',' + var + ',' + scen + ',' + score)
	point = point + 1;
	   
	