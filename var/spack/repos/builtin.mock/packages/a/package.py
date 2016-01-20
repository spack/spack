from spack import *

class A(Package):
    """Simple package with no dependencies"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        pass
