from spack import *


class SeparateBuildBuild(Package):
    """This dependency is only required for building dependents. It requires
    a package configuration that conflicts with the link dependency of its
    dependent, but should succeed anyways since this package does not need to
    be linked.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'SeparateBuildBuild1.0')

    depends_on('separate-build-link~X')

    def install(self, spec, prefix):
        pass
