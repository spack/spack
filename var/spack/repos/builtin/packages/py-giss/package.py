from spack import *

class PyGiss(Package):
    """Misc. Python Stuff."""

    homepage = "https://github.com/citibeth/pygiss"
    url      = "https://github.com/citibeth/pygiss/tarball/v0.1.0"

    version('0.1.0', '2eb907ca0af9fd1463357740df7c4ac0')

    # Requires python@3:
    extends('python')

    depends_on('py-numpy+blas+lapack')
    depends_on('py-netcdf')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
