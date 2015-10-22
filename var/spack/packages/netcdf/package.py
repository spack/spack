from spack import *

class Netcdf(Package):
    """NetCDF is a set of software libraries and self-describing, machine-independent
        data formats that support the creation, access, and sharing of array-oriented
        scientific data."""

    homepage = "http://www.unidata.ucar.edu/software/netcdf/"
    url      = "ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.3.3.tar.gz"

    version('4.3.3', '5fbd0e108a54bd82cb5702a73f56d2ae')

    patch('netcdf-4.3.3-mpi.patch')

    # Dependencies:
        # >HDF5
    depends_on("hdf5")

    def install(self, spec, prefix):
        with working_dir('spack-build', create=True):
            cmake('..',
                "-DCMAKE_INSTALL_PREFIX:PATH=%s" % prefix,
                "-DENABLE_DAP:BOOL=OFF", # Disable DAP.
                "-DBUILD_SHARED_LIBS:BOOL=OFF") # Don't build shared libraries (use static libs).

            make()
            make("install")
