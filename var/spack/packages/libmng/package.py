from spack import *

class Libmng(Package):
    """libmng -THE reference library for reading, displaying, writing
       and examining Multiple-Image Network Graphics.  MNG is the animation
       extension to the popular PNG image-format."""
    homepage = "http://sourceforge.net/projects/libmng/"
    url      = "http://downloads.sourceforge.net/project/libmng/libmng-devel/2.0.2/libmng-2.0.2.tar.gz"

    version('2.0.2', '1ffefaed4aac98475ee6267422cbca55')

    depends_on("jpeg")
    depends_on("zlib")
    depends_on("lcms")

    def patch(self):
        # jpeg requires stdio to beincluded before its headrs.
        filter_file(r'^(\#include \<jpeglib\.h\>)', '#include<stdio.h>\n\\1', 'libmng_types.h')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
