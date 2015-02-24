from spack import *

class PyMx(Package):
    """The eGenix.com mx Base Distribution for Python is a collection of professional quality software tools which enhance Python's usability in many important areas such as fast text searching, date/time processing and high speed data types."""
    homepage = "http://www.egenix.com/products/python/mxBase/"
    url      = "https://downloads.egenix.com/python/egenix-mx-base-3.2.8.tar.gz"

    version('3.2.8', '9d9d3a25f9dc051a15e97f452413423b')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
