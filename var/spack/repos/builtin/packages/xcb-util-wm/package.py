from spack import *


class XcbUtilWm(Package):
    """Extension libraries for xcb-util to make xcb more usable. This one adds
    window manager helpers for ICCCM"""

    homepage = "https://xcb.freedesktop.org/XcbUtil"
    url      = "https://xcb.freedesktop.org/dist/xcb-util-wm-0.4.1.tar.gz"

    version('0.4.1', '0831399918359bf82930124fa9fd6a9b')
    version('0.4.0', '647ef0ac130fe2f49ae465dd4b014c68')
    version('0.3.9', 'b551139701bd3b847dfa3583031815c6')

    depends_on("libxcb")
    depends_on("xcb-util")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
