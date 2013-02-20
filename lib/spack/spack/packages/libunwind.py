from spack import *

class Libunwind(Package):
    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"
    md5      = "fb4ea2f6fbbe45bf032cd36e586883ce"

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
