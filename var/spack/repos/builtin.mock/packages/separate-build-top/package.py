from spack import *


class SeparateBuildTop(Package):
    """The top of a dependency hierarchy which is intended to test whether
    Spack can concretize two conflicting instances of a package when one of
    them is needed only by a build dependency.
    """

    homepage = "http://www.example.com"
    url      = "http://www.example.com/a-1.0.tar.gz"

    version('1.0', 'SeparateBuildTop1.0')

    depends_on('separate-build-link+X')
    depends_on('separate-build-build', type='build')

    def install(self, spec, prefix):
        pass
