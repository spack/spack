from spack import *

class PyGiss(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/pygiss"
    url      = "https://github.com/citibeth/pygiss/tarball/v0.1.0"

    version('0.1.0', '766c88600096fc35acfb2174a981e634')

    # Requires python@3:
    extends('python')

    depends_on('py-numpy+blas+lapack')
    depends_on('py-netcdf')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
