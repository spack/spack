from spack import *

class Jpeg(Package):
    """jpeg library"""
    homepage = "http://www.ijg.org"
    url      = "http://www.ijg.org/files/jpegsrc.v9a.tar.gz"

    version('9a', '3353992aecaee1805ef4109aadd433e7')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
