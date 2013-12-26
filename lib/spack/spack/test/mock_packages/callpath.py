from spack import *

class Callpath(Package):
    homepage = "https://github.com/tgamblin/callpath"
    url      = "http://github.com/tgamblin/callpath-1.0.tar.gz"

    versions = { 0.8 : 'foobarbaz',
                 0.9 : 'foobarbaz',
                 1.0 : 'foobarbaz' }

    depends_on("dyninst")
    depends_on("mpi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
