from spack import *

class Imagemagick(Package):
    """ImageMagick is a image processing library"""
    homepage = "http://www.imagemagic.org"

    #-------------------------------------------------------------------------
    # ImageMagick does not keep around anything but *-10 versions, so
    # this URL may change.  If you want the bleeding edge, you can
    # uncomment it and see if it works but you may need to try to
    # fetch a newer version (-6, -7, -8, -9, etc.) or you can stick
    # wtih the older, stable, archived -10 versions below.
    #
    # TODO: would be nice if spack had a way to recommend avoiding a
    # TODO: bleeding edge version, but not comment it out.
    # -------------------------------------------------------------------------
    # version('6.9.0-6', 'c1bce7396c22995b8bdb56b7797b4a1b',
    # url="http://www.imagemagick.org/download/ImageMagick-6.9.0-6.tar.bz2")

    #-------------------------------------------------------------------------
    # *-10 versions are archived, so these versions should fetch reliably.
    # -------------------------------------------------------------------------
    version('6.8.9-10', 'aa050bf9785e571c956c111377bbf57c',
            url="http://sourceforge.net/projects/imagemagick/files/old-sources/6.x/6.8/ImageMagick-6.8.9-10.tar.gz/download")

    depends_on('libtool')
    depends_on('jpeg')
    depends_on('libpng')
    depends_on('freetype')
    depends_on('fontconfig')
    depends_on('libtiff')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
