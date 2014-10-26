from spack import *

class Freetype(Package):
    """Font package"""
    homepage = "http://http://www.freetype.org"
    url      = "http://download.savannah.gnu.org/releases/freetype/freetype-2.5.3.tar.gz"

    version('2.5.3'  , 'cafe9f210e45360279c730d27bf071e9')

    depends_on('libpng')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
