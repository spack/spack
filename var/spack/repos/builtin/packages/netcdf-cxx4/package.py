from spack import *

class NetcdfCxx4(Package):
    """C++ interface for NetCDF4"""
    homepage = "http://www.unidata.ucar.edu/software/netcdf"
    url      = "https://www.github.com/unidata/netcdf-cxx4/tarball/v4.3.0"

    version('4.2.1', 'd019853802092cf686254aaba165fc81')
    version('4.3.0', '0dde8b9763eecdafbd69d076e687337e')

    depends_on('netcdf')
    depends_on("autoconf")

    def install(self, spec, prefix):
        which('autoreconf')('-ivf')    # Rebuild to prevent problems of inconsistency in git repo
        configure('--prefix=%s' % prefix)
        make()
        make("install")
