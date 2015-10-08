from spack import *

class Libxcb(Package):
    """The X protocol C-language Binding (XCB) is a replacement 
    for Xlib featuring a small footprint, latency hiding, direct 
    access to the protocol, improved threading support, and 
    extensibility."""

    homepage = "http://xcb.freedesktop.org/"
    url      = "http://xcb.freedesktop.org/dist/libxcb-1.11.tar.gz"

    version('1.11', '1698dd837d7e6e94d029dbe8b3a82deb')
    version('1.11.1', '118623c15a96b08622603a71d8789bf3')
    depends_on("python")
    depends_on("xcb-proto")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
