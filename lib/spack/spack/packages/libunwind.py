from spack import *

class Libunwind(Package):
    homepage = "http://www.nongnu.org/libunwind/"
    url      = "http://download.savannah.gnu.org/releases/libunwind/libunwind-1.1.tar.gz"

    versions = { '1.1' : 'fb4ea2f6fbbe45bf032cd36e586883ce' }

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
