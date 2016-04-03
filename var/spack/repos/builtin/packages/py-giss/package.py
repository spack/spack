from spack import *

class PyGiss(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/pygiss"
    url      = "https://github.com/citibeth/pygiss/tarball/v0.1.0"

    version('0.1.1', '172d468690a8b8f474884d7a60064bc7')

    # Requires python@3:
    extends('python')

    depends_on('py-numpy+blas+lapack')
    depends_on('py-netcdf')
    depends_on('py-matplotlib')
    depends_on('py-basemap')
    depends_on('py-proj')
    depends_on('py-scipy')
    depends_on('py-six')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
