from spack import *

class PyRpy2(Package):
    """rpy2 is a redesign and rewrite of rpy. It is providing a low-level interface to R from Python, a proposed high-level interface, including wrappers to graphical libraries, as well as R-like structures and functions."""
    homepage = "https://pypi.python.org/pypi/rpy2"
    url      = "https://pypi.python.org/packages/source/r/rpy2/rpy2-2.5.4.tar.gz"

    version('2.5.4', '115a20ac30883f096da2bdfcab55196d')
    version('2.5.6', 'a36e758b633ce6aec6a5f450bfee980f')

    extends('python')
    depends_on('py-setuptools')

    depends_on('R')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
