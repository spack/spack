from spack import *

class NetcdfCxx4(Package):
    """C++ interface for NetCDF4"""
    homepage = "http://www.unidata.ucar.edu/downloads/netcdf/netcdf-cxx/index.jsp"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-cxx4-4.2.tar.gz"

    version('4.2', 'd019853802092cf686254aaba165fc81')

    depends_on('netcdf')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
