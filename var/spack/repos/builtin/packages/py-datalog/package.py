from spack import *

class PyDatalog(Package):
    """Description"""

    homepage = 'https://pypi.python.org/pypi/pyDatalog/'
    url      = 'https://pypi.python.org/packages/09/0b/2670eb9c0027aacfb5b5024ca75e5fee2f1261180ab8797108ffc941158a/pyDatalog-0.17.1.zip'

    version('0.17.1', '6b2682301200068d208d6f2d01723939')

    extends('python')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' %prefix)
