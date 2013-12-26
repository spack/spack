from spack import *

class Mpileaks(Package):
    homepage = "http://www.llnl.gov"
    url      = "http://www.llnl.gov/mpileaks-1.0.tar.gz"

    depends_on("mpich")
    depends_on("callpath")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
