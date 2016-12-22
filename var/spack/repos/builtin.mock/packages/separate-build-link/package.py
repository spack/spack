from spack import *


class SeparateBuildLink(Package):
    """Package with a variant, so different dependents can require different
       instances."""

    homepage = "http://www.SeparateBuildLink.com"
    url      = "http://www.SeparateBuildLink.com/SeparateBuildLink-1.0.tar.gz"

    version('1.0', 'SeparateBuildLink1.0')

    variant('X', default=True, description='test variant')

    def install(self, spec, prefix):
        pass
