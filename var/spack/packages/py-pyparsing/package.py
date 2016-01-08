from spack import *

class PyPyparsing(Package):
    """A Python Parsing Module."""
    homepage = "https://pypi.python.org/pypi/pyparsing"
    url      = "https://pypi.python.org/packages/source/p/pyparsing/pyparsing-2.0.3.tar.gz"

    version('2.0.3', '0fe479be09fc2cf005f753d3acc35939')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
