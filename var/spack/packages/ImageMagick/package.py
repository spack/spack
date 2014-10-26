from spack import *

class Imagemagick(Package):
    """ImageMagick is a image processing library"""
    homepage = "http://www.imagemagic.org"
    url      = "http://www.imagemagick.org/download/ImageMagick-6.8.9-8.tar.gz"

    version('6.8.9-8', '74aa203286bfb8aaadd320f787eea64e')

    depends_on(libtool)
    depends_on(jpeg)
    depends_on(libpng)
    depends_on(freetype)
    depends_on(fontconfig)
    depends_on(libtiff)

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
