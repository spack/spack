from spack import *

class PyBottleneck(Package):
    """Bottleneck is a collection of fast NumPy array functions written in Cython."""
    homepage = "https://pypi.python.org/pypi/Bottleneck/1.0.0"
    url      = "https://pypi.python.org/packages/source/B/Bottleneck/Bottleneck-1.0.0.tar.gz"

    version('1.0.0', '380fa6f275bd24f27e7cf0e0d752f5d2')

    extends('python')
    depends_on('py-numpy')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
