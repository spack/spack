from spack import *


class SeparateBuildTop(Package):
    """Simple package with no dependencies"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'SeparateBuildTop1.0')

    depends_on('separate-build-link+X')
    depends_on('separate-build-build', type='build')

    def install(self, spec, prefix):
        pass
