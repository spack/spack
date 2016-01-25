from spack import *


class Dtlink4(Package):
    """Simple package which acts as a link dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtlink4-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    def install(self, spec, prefix):
        pass
