from spack import *

class Callpath(Package):
    homepage = "https://github.com/tgamblin/callpath"
    url      = "http://github.com/tgamblin/callpath-0.2.tar.gz"

    depends_on("dyninst")
    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
