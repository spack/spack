from spack import *

class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    versions = { 1.0 : 'foobarbaz',
                 2.1 : 'foobarbaz',
                 2.2 : 'foobarbaz',
                 2.3 : 'foobarbaz' }

    depends_on("mpi")
    depends_on("callpath")

    def install(self, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
