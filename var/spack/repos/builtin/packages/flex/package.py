from spack import *

class Flex(Package):
    """Flex is a tool for generating scanners."""

    homepage = "http://flex.sourceforge.net/"
    url      = "http://download.sourceforge.net/flex/flex-2.5.39.tar.gz"

    version('2.5.39', 'e133e9ead8ec0a58d81166b461244fde')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
