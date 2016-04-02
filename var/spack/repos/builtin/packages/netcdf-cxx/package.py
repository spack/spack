from spack import *

class NetcdfCxx(Package):
    “””Deprecated C++ compatibility bindings for NetCDF.
    These do NOT read or write NetCDF-4 files, and are no longer
    maintained by Unidata.  Developers should migrate to current
    NetCDF C++ bindings, in Spack package netcdf-cxx4.”””

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx-4.2.tar.gz"

    version('4.2', 'd32b20c00f144ae6565d9e98d9f6204c')

    depends_on('netcdf')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
