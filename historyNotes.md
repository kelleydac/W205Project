###Mounting NEXDCP30 data on EMR

	git clone git://github.com/s3fs-fuse/s3fs-fuse.git

	cd s3fs-fuse
	
	./autogen.sh
	
	./configure
	
	make
	
	sudo make install
	
	/usr/bin/s3fs -o default_acl='public read' nasanex:/NEX-DCP30 /mnt/s3-nexdcp30/ -o public_bucket=1
	
How do we make this readable by users other than root?

Also need autoconf

	sudo yum install automake
	sudo yum install gcc-c++
	sudo yum install fuse libcurl libxml-2.0
	
Doesn't recognize libraries

###Try a Ubuntu instance

	sudo apt-get update
	sudo apt-get install git
	git clone git://github.com/s3fs-fuse/s3fs-fuse.git
	sudo apt-get install make gcc g++ pkg-config libfuse-dev libcurl4-openssl-dev libxml2-dev automake
	
Still can't mount it readable by anyone other than root

	sudo apt-get install python-pip python2.7-dev cython libhdf5-serial-dev
	sudo pip install numpy h5py

Copying a file over as root and chmod'ing it makes it readable

can get data using h5py! [yay]

sudo mkdir -p /mnt/s3

Try this next:

	sudo /usr/local/bin/s3fs -o default_acl='public 	read',allow_other,uid=1000,gid=1000 nasanex:/NEX-	DCP30 /mnt/s3/ -o public_bucket=1

Works [yay again!]

###Data layout
historical  rcp26  rcp45  rcp60  rcp85

/mnt/s3/NEX-quartile/historical/mon/atmos/{pr,tasmax,tasmin}/r1i1p1/v1.0/CONUS/pr_{ens-avg,quartile25,quartile50,quartile75}_amon_historical_CONUS_195001-195412.nc

up to

200501-200512

/mnt/s3/NEX-quartile/rcp26/mon/atmos/{pr,tasmax,tasmin}/r1i1p1/v1.0/CONUS/pr_{ens-avg,quartile25,quartile50,quartile75}_amon_rcp26_CONUS_202101-202512,nc

up to 
209601-209912.nc

###Extracting Data
Create an HDF file

Put the row and column in the filename

Copy over the lat and lon for the point in question

add the start date 

add the pr, tasmax, and tasmin data to the file

###Opening the file

	froot='/mnt/s3/NEX-quartile/'
	scen='historical'
	flink1='/mon/atmos/'
	myVar='tasmax'	
	flink2='/r1i1p1/v1.0/CONUS/'
	flink3='_ens-avg_amon_'
	flink4='_CONUS_'
	dateRange='196501-196912'
	fext='.nc'
	f4=h5py.File(froot+scen+flink1+myVar+flink2+myVar+flink3+scen+flink4+dateRange+fext,'r')
###To Do
Create template NetCDF4 file in bootstrap -- done

Write scores to NetCDF4 file

Push to S3

Split to separate python files

mapper checks if targets defined and loads if not

mapper takes point and generates key as location and scenario, value as var/score

reducer consolidates scores over vars to generate a single aggregate score as scen/lat/lon/score

reader consoldiates scores to single nc file

####6 Dec 2014
Input tag file: s3://kelley-w205/Project/Input/tags.txt

To run local MR job:

	python genTags.py 2024 1664 300 10 | python where2Move.py
	
Job arguments:
	
	-files s3://kelley-w205/Project/corrMapper.py -mapper corrMapper.py -reducer aggregate -input s3://kelley-w205/Project/Input/tags.txt -output s3://kelley-w205/Project/Output/6dec2014_1/
	
4:15 per point per node

example rcp85 tasmin -- 1.00355

Closing nc file after reading it allows >2 data reads

####8 Dec 2014
Finally works with tags1Scen

medium cluster 
50 min to boot

tags1Point -- 25 min (2)

4 Points -- 92 min (4)

100 tags -- 181 minutes (3)

####Large cluster
31 min to boot

64 points -- 122 minutes (5)

	-files s3://kelley-w205/Project/corrMapper.py -mapper corrMapper.py -reducer NONE -input s3://kelley-w205/Project/Input/tags64.txt -output s3://kelley-w205/Project/Output/8dec2014_5/

####XLarge cluster

29 min to boot

128 points 73 minutes (6)

####14 Dec 2014
Same 128 points, but use 4 xlarge core instances

37 min to boot

Some parts were successful but some failed -- collision opening files?

Try again with only 2

26 min to boot 81 min to run

Try tags from year 2040 -- bug in file name generator

Read some and failed but did generate some output -- try with tags128

tags20 -- 2 hr 29 m

###Viz
For smaller spatial datasets, usr R maps

Aggregate output by location -- so mapper needs to spit out lat/lon and value as scen/var/score

reducer then converts to lat/lon/var scen/score

And then we convert text output to CSV

Convert from indices to actual lat/lon

	lat = 24.0625+lat_idx*0.008333333
	lon = 234.979166 + lon_idx*0.00833333

point,lat,lon,year,var,scen,score

Load to R

Get range of lat, lon

Display corresponding map

Add data with points

	SF10<-get_map('San Francisco', zoom=10)
	sfmap10<-ggmap(SF10, extent='device',legend='topleft')
	sfmap10+geom_point(aes(x=lon-360,y=lat,col="red",size=2),data=df)