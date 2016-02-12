from spack import *

class OptionalDepTest3(Package):
    """Depends on the optional-dep-test package"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/optional-dep-test-3-1.0.tar.gz"

    version('1.0', '0123456789abcdef0123456789abcdef')

    variant('var', default=False)

    depends_on('a', when='~var')
    depends_on('b', when='+var')

    def install(self, spec, prefix):
        pass
