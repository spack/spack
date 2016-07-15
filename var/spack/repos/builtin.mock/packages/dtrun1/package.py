from spack import *


class Dtrun1(Package):
    """Simple package which acts as a run dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtrun1-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtlink5')
    depends_on('dtrun3', type='run')

    def install(self, spec, prefix):
        pass
