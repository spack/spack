from spack import *

class Ghostscript(Package):
    """an interpreter for the PostScript language and for PDF. """
    homepage = "http://ghostscript.com/"
    url      = "http://downloads.ghostscript.com/public/old-gs-releases/ghostpdl-9.16.tar.gz"

#    version('9.16', '829319325bbdb83f5c81379a8f86f38f')
    version('9.16', '818c87e31f7562aaa97397d3d0cc20a1')

    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

