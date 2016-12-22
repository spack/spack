from spack import *


class SeparateBuildBuild(Package):
    """Simple package with no dependencies"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'SeparateBuildBuild1.0')

    depends_on('separate-build-link~X')

    def install(self, spec, prefix):
        pass
