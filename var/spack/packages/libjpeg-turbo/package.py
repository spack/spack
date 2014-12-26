from spack import *

class LibjpegTurbo(Package):
    """libjpeg-turbo is a fork of the original IJG libjpeg which uses
       SIMD to accelerate baseline JPEG compression and
       decompression. libjpeg is a library that implements JPEG image
       encoding, decoding and transcoding."""
    homepage = "http://libjpeg-turbo.virtualgl.org"
    url      = "http://downloads.sourceforge.net/libjpeg-turbo/libjpeg-turbo-1.3.1.tar.gz"

    version('1.3.1', '2c3a68129dac443a72815ff5bb374b05')

    # Can use either of these.
    depends_on("yasm")
    depends_on("nasm")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
