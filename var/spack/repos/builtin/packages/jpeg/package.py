from spack import *

class Jpeg(Package):
    """libjpeg is a widely used free library with functions for handling the
    JPEG image data format. It implements a JPEG codec (encoding and decoding)
    alongside various utilities for handling JPEG data."""

    homepage = "http://www.ijg.org"
    url      = "http://www.ijg.org/files/jpegsrc.v9b.tar.gz"

    version('9b', '6a9996ce116ec5c52b4870dbcd6d3ddb')
    version('9a', '3353992aecaee1805ef4109aadd433e7')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("test")
        make("install")
