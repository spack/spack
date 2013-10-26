from spack import *

class Callpath(Package):
    homepage = "https://github.com/tgamblin/callpath"
    url      = "http://github.com/tgamblin/callpath-0.2.tar.gz"
    md5      = "foobarbaz"

    versions = [0.8, 0.9, 1.0]

    depends_on("dyninst")
    depends_on("mpich")

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
