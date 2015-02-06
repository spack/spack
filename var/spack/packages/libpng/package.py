from spack import *

class Libpng(Package):
    """libpng graphics file format"""
    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://sourceforge.net/projects/libpng/files/libpng16/1.6.15/libpng-1.6.15.tar.gz/download"

    version('1.6.15', '829a256f3de9307731d4f52dc071916d')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
