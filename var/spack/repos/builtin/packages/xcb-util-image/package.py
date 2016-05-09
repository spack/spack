from spack import *

class XcbUtilImage(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-image-0.3.8.tar.gz"

    version('0.4.0', '32c9c2f72ebd58a2b2e210f27fee86f7')
    version('0.3.9', '0bdfcea4ce0666b45d2d64c1f1e25801')
    version('0.3.8', 'b6d1359b5851ea319a81e15c18f34aeb')

    # FIXME: Add dependencies if this package requires them.
    depends_on("libxcb")
    depends_on("xcb-util")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
