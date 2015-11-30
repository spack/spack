from spack import *

class Lcms(Package):
    """Little cms is a color management library. Implements fast
       transforms between ICC profiles. It is focused on speed, and is
       portable across several platforms (MIT license)."""
    homepage = "http://www.littlecms.com"
    url      = "http://downloads.sourceforge.net/project/lcms/lcms/2.6/lcms2-2.6.tar.gz"

    version('2.6', 'f4c08d38ceade4a664ebff7228910a33')

    depends_on("jpeg")
    depends_on("libtiff")
    depends_on("zlib")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
