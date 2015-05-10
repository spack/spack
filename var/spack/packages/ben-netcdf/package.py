from spack import *
import os

class BenNetcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent 
	data formats that support the creation, access, and sharing of array-oriented 
	scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf/"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    # Dependencies:
	# >HDF5
    depends_on("ben-hdf5")
	
    parallel = False

    def setup_dependent_environment(self, module, spec, dep_spec):
        os.environ['NETCDF'] = self.prefix

    def install(self, spec, prefix):    
        configure(
		"--prefix=%s" % prefix, 
		"CPPFLAGS=-I%s/include" % spec['ben-hdf5'].prefix, # Link HDF5's include dir.
		"LDFLAGS=-L%s/lib" % spec['ben-hdf5'].prefix) # Link HDF5's lib dir.
		
        make()
        make('check')
        make("install")
        make('installcheck')

	# Check the newly installed netcdf package. Currently disabled.
	# make("check")
