from spack import *

class Libpng(Package):
    """libpng graphics file format"""
    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://sourceforge.net/projects/libpng/files/libpng16/1.6.14/libpng-1.6.14.tar.gz/download"

    version('1.6.14', '2101b3de1d5f348925990f9aa8405660')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
