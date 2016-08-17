from spack import *


class Dtlink1(Package):
    """Simple package which acts as a link dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtlink1-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtlink3')

    def install(self, spec, prefix):
        pass
