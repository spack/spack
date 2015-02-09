from spack import *

class Libpng(Package):
    """libpng graphics file format"""
    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://prdownloads.sourceforge.net/libpng/libpng-1.6.16.tar.gz?download"

    version('1.6.16', '1a4ad377919ab15b54f6cb6a3ae2622d')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
