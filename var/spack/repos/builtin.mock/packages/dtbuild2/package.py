from spack import *


class Dtbuild2(Package):
    """Simple package which acts as a build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtbuild2-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        pass
