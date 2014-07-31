from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_4.0.0.tar.gz"

    version('4.0.0', 'd00301c078cba57ef68613be32ceea2f')
    version('4.1.0', '5a248298b395b329e2371bf25366115c')

    parallel = False

    depends_on("boost")

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

