from spack import *

class Imagemagick(Package):
    """ImageMagick is a image processing library"""
    homepage = "http://www.imagemagic.org"
    url      = "http://www.imagemagick.org/download/ImageMagick-6.8.9-9.tar.gz"

    version('6.8.9-9', 'e63fed3e3550851328352c708f800676')

    depends_on('libtool')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('fontconfig')
#   depends_on('libtiff')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
