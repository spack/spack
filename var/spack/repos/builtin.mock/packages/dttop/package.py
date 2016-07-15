from spack import *


class Dttop(Package):
    """Package with a complicated dependency tree"""

    homepage = "http://www.example.com"
    url = "http://www.example.com/dttop-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    depends_on('dtbuild1', type='build')
    depends_on('dtlink1')
    depends_on('dtrun1', type='run')

    def install(self, spec, prefix):
        pass
