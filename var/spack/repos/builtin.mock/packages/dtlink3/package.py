from spack import *


class Dtlink3(Package):
    """Simple package which acts as a link dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtlink3-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtbuild2', type='build')
    depends_on('dtlink4')

    def install(self, spec, prefix):
        pass
