from spack import *

class Libpng(Package):
    """libpng graphics file format"""
    homepage = "http://www.libpng.org/pub/png/libpng.html"
    url      = "http://download.sourceforge.net/libpng/libpng-1.6.16.tar.gz"

    version('1.6.16', '1a4ad377919ab15b54f6cb6a3ae2622d')
    version('1.6.15', '829a256f3de9307731d4f52dc071916d')
    version('1.6.14', '2101b3de1d5f348925990f9aa8405660')
    version('1.5.26', '3ca98347a5541a2dad55cd6d07ee60a9')
    version('1.4.19', '89bcbc4fc8b31f4a403906cf4f662330')
    version('1.2.56', '9508fc59d10a1ffadd9aae35116c19ee')

    depends_on('zlib')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
