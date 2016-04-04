from spack import *

class PyMpmath(Package):
    """A Python library for arbitrary-precision floating-point arithmetic."""
    homepage = "http://mpmath.org"
    url      = "https://pypi.python.org/packages/source/m/mpmath/mpmath-all-0.19.tar.gz"

    version('0.19', 'd1b7e19dd6830d0d7b5e1bc93d46c02c')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
