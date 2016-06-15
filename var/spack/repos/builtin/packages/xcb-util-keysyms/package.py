from spack import *


class XcbUtilKeysyms(Package):
    """Standard X key constants and conversion to/from keycodes."""

    homepage = "https://xcb.freedesktop.org/XcbUtil"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-keysyms-0.3.9.tar.gz"

    version('0.4.0', '2decde7b02b4b3bde99a02c17b64d5dc')
    version('0.3.9', 'ec56b17970b17e84418d0cd2b55562b2')

    depends_on("libxcb")
    depends_on("xcb-util")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
