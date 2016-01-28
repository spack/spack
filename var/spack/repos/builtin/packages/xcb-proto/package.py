from spack import *

class XcbProto(Package):
    """Protocol for libxcb"""

    homepage = "http://xcb.freedesktop.org/"
    url      = "http://xcb.freedesktop.org/dist/xcb-proto-1.11.tar.gz"

    version('1.11', 'c8c6cb72c84f58270f4db1f39607f66a')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
