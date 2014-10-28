from spack import *

class Jpeg(Package):
    """jpeg library"""
    homepage = "http://www.ijg.org"
    url      = "http://www.ijg.org/files/jpegsrc.v9a.tar.gz"

    version('9', 'b397211ddfd506b92cd5e02a22ac924d')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
