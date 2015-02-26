from spack import *

class Dri2proto(Package):
    """DRI2 Protocol Headers."""
    homepage = "http://http://cgit.freedesktop.org/xorg/proto/dri2proto/"
    url      = "http://xorg.freedesktop.org/releases/individual/proto/dri2proto-2.8.tar.gz"

    version('2.8', '19ea18f63d8ae8053c9fa84b60365b77')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
