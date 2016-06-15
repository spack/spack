from spack import *


class XcbUtilImage(Package):
    """Port of Xlib's XImage and XShmImage functions"""

    homepage = "https://xcb.freedesktop.org/XcbUtil"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-image-0.3.8.tar.gz"

    version('0.4.0', '32c9c2f72ebd58a2b2e210f27fee86f7')
    version('0.3.9', '0bdfcea4ce0666b45d2d64c1f1e25801')
    version('0.3.8', 'b6d1359b5851ea319a81e15c18f34aeb')

    depends_on("libxcb")
    depends_on("xcb-util")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
