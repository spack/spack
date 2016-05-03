# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install xcb-util
#
# You can always get back here to change things with:
#
#     spack edit xcb-util
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class XcbUtil(Package):
    """FIXME: put a proper description of your package here."""
    # FIXME: add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-0.4.0.tar.gz"

    version('0.4.0', '157d82738aa89934b6adaf3ca508a0f5')
    version('0.3.9', 'ca04b25d913239a3ef94b688f7ac38cd')

    # FIXME: Add dependencies if this package requires them.
    depends_on("libxcb")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
