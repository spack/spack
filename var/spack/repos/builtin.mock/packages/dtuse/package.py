from spack import *


class Dtuse(Package):
    """Simple package which uses dttop"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dtuse-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dttop')

    def install(self, spec, prefix):
        pass
