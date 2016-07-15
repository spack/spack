from spack import *


class Dtbuild3(Package):
    """Simple package which acts as a build dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtbuild3-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        pass
