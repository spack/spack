from spack import *

class B(Package):
    """Simple package with no dependencies"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/b-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        pass
