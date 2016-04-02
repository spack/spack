from spack import *

class NetcdfCxx(Package):
    """C++ compatibility bindings for NetCDF"""
    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx-4.2.tar.gz"

    version('4.2', 'd32b20c00f144ae6565d9e98d9f6204c')

    depends_on('netcdf')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
