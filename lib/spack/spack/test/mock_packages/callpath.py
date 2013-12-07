from spack import *

class Callpath(Package):
    homepage = "https://github.com/tgamblin/callpath"
    url      = "http://github.com/tgamblin/callpath-0.2.tar.gz"
    md5      = "foobarbaz"

    versions = { 0.8 : 'bf03b33375afa66fe0efa46ce3f4b17a',
                 0.9 : 'bf03b33375afa66fe0efa46ce3f4b17a',
                 1.0 : 'bf03b33375afa66fe0efa46ce3f4b17a' }

    depends_on("dyninst")
    depends_on("mpi")

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
