from spack import *

class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"
    md5      = "foobarbaz"

    versions = { 1.0 : None,
                 2.1 : None,
                 2.2 : None,
                 2.3 : None }

    depends_on("mpi")
    depends_on("callpath")

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
