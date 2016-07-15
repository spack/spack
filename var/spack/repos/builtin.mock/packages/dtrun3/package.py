from spack import *


class Dtrun3(Package):
    """Simple package which acts as a run dependency"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtrun3-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtbuild3', type='build')

    def install(self, spec, prefix):
        pass
