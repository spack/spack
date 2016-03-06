from spack import *

class NetcdfFortran(Package):
    """Fortran interface for NetCDF4"""

    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "http://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.4.3.tar.gz"

    version('4.4.3', 'bfd4ae23a34635b273d3eb0d91cbde9e')

    depends_on('netcdf')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
