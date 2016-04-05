from spack import *

class PyNetworkx(Package):
    """NetworkX is a Python package for the creation, manipulation, and study of the structure, dynamics, and functions of complex networks."""
    homepage = "http://networkx.github.io/"
    url      = "https://pypi.python.org/packages/source/n/networkx/networkx-1.11.tar.gz"

    version('1.11', '6ef584a879e9163013e9a762e1cf7cd1')

    extends('python')

    depends_on('py-decorator')

    def install(self, spec, prefix):
        python('setup.py', 'install', '--prefix=%s' % prefix)
