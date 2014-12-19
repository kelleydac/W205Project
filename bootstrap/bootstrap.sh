#! /bin/bash
# setup commands for Redhat EMR engine for climate data extractor project
# created 27 October 2014 Doug Kelley for MIDS W205 project
# working version 9 nov 2014

sudo yum -y update
sudo yum -y install git automake libcurl-devel


#HDF5 -- revert to 1.8.14 16 nov 2014
wget http://www.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8.13/src/hdf5-1.8.13.tar.gz
gzip -dc hdf5-1.8.13.tar.gz | tar xf -
cd hdf5-1.8.13
./configure --prefix=/usr/local
make
sudo make install

echo "completed hdf5 installation"

sudo yum -y install python27-pip

# load h5py and mrjob
sudo pip2.7 install cython h5py mrjob

echo "install cython h5py and mrjob"

# install s3fs
git clone git://github.com/s3fs-fuse/s3fs-fuse.git

cd s3fs-fuse

./autogen.sh
./configure
make
sudo make install

echo "s3fs installed"

# mount the NASA data
sudo mkdir -p /mnt/s3
sudo /usr/local/bin/s3fs -o default_acl='public read',allow_other,uid=498,gid=501 nasanex:/NEX-DCP30 /mnt/s3 -o public_bucket=1

sudo sh -c  "echo '/usr/local/lib' > /etc/ld.so.conf.d/usrlocal.conf"
sudo ldconfig -v

# everything should be mounted now; let's add some swap space
#export SWAPSIZE=2048
#export SWAPFILE=/mnt/swapfile
sudo dd if=/dev/zero of=/mnt/swapfile bs=1M count=2048
sudo chmod 0600 /mnt/swapfile

sudo /sbin/mkswap /mnt/swapfile
sudo /sbin/swapon /mnt/swapfile

echo "Swap space added"

# Add code to extract target signatures
cd ~
export SOURCEROOT=/mnt/s3/NEX-quartile/historical/mon/atmos/pr/r1i1p1/v1.0/CONUS/
export SOURCEFILE=pr_ens-avg_amon_historical_CONUS_196001-196412.nc

python27 -c "import h5py; f=h5py.File('$SOURCEROOT$SOURCEFILE','r'); target=f['pr'][36:48,1664,300]; target.tofile(open('prTarget.txt','w'),'\n')"

export SOURCEROOT=/mnt/s3/NEX-quartile/historical/mon/atmos/tasmin/r1i1p1/v1.0/CONUS/
export SOURCEFILE=tasmin_ens-avg_amon_historical_CONUS_196001-196412.nc

python27 -c "import h5py; f=h5py.File('$SOURCEROOT$SOURCEFILE','r'); target=f['tasmin'][36:48,1664,300]; target.tofile(open('tasminTarget.txt','w'),'\n')"

export SOURCEROOT=/mnt/s3/NEX-quartile/historical/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/
export SOURCEFILE=tasmax_ens-avg_amon_historical_CONUS_196001-196412.nc

python27 -c "import h5py; import numpy; f=h5py.File('$SOURCEROOT$SOURCEFILE','r'); target=f['tasmax'][36:48,1664,300]; target.tofile(open('tasmaxTarget.txt','w'),'\n')" 

# Now set up target file
#python27 -c "import h5py; import numpy; fin=h5py.File('$SOURCEROOT$SOURCEFILE','r'); fout=h5py.File('targetScore.nc','w'); nlats = fin['lat'].size; nlons = fin['lon'].size; fout.create_dataset('lat', data=fin['lat']); fout.create_dataset('lon', data=fin['lon']); fout.create_dataset('rcp26', data=numpy.zeros([nlats,nlons])); fout.create_dataset('rcp45', data=numpy.zeros([nlats,nlons])); fout.create_dataset('rcp60', data=numpy.zeros([nlats,nlons])); fout.create_dataset('rcp85', data=numpy.zeros([nlats,nlons]));"
