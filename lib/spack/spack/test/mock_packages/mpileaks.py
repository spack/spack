from spack import *

class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"
    md5      = "foobarbaz"

    versions = [1.0, 2.1, 2.2, 2.3]

    depends_on("mpich")
    depends_on("callpath")

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
