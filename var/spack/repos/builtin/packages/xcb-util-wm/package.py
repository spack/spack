# FIXME:
# This is a template package file for Spack.  We've conveniently
# put "FIXME" labels next to all the things you'll want to change.
#
# Once you've edited all the FIXME's, delete this whole message,
# save this file, and test out your package like this:
#
#     spack install xcb-util-wm
#
# You can always get back here to change things with:
#
#     spack edit xcb-util-wm
#
# See the spack documentation for more information on building
# packages.
#
from spack import *

class XcbUtilWm(Package):
    """Extension libraries for xcb-util to make xcb more usable. This one adds window manager helpers for ICCCM"""
    homepage = "https://xcb.freedesktop.org/"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-wm-0.4.1.tar.gz"

    version('0.4.1', '0831399918359bf82930124fa9fd6a9b')
    version('0.4.0', '647ef0ac130fe2f49ae465dd4b014c68')
    version('0.3.9', 'b551139701bd3b847dfa3583031815c6')

    # FIXME: Add dependencies if this package requires them.
    depends_on("libxcb")
    depends_on("xcb-util")

    def install(self, spec, prefix):
        # FIXME: Modify the configure line to suit your build system here.
        configure('--prefix=%s' % prefix)

        # FIXME: Add logic to build and install here
        make()
        make("install")
