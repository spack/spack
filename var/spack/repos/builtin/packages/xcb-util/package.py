from spack import *


class XcbUtil(Package):
    """The xcb-util module provides a number of libraries which sit on top of
    libxcb, the core X protocol library, and some of the extension libraries.
    These experimental libraries provide convenience functions and interfaces
    which make the raw X protocol more usable. Some of the libraries also
    provide client-side code which is not strictly part of the X protocol but
    which have traditionally been provided by Xlib."""

    homepage = "https://xcb.freedesktop.org/XcbUtil"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.gz"

    version('0.4.0', '157d82738aa89934b6adaf3ca508a0f5')
    version('0.3.9', 'ca04b25d913239a3ef94b688f7ac38cd')

    depends_on("libxcb")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
