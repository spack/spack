from spack import *

class PyNetcdf(Package):
    """Python interface to the netCDF Library."""
    homepage = "http://unidata.github.io/netcdf4-python"
    url      = "https://github.com/Unidata/netcdf4-python/tarball/v1.2.3.1rel"

    version('1.2.3.1', '4fc4320d4f2a77b894ebf8da1c9895af')

    extends('python')
    depends_on('py-numpy')
    depends_on('py-cython')
    depends_on('netcdf')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
