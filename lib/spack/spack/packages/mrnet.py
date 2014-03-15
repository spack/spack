from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_4.0.0.tar.gz"

    versions = { '4.0.0' : 'd00301c078cba57ef68613be32ceea2f', }

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make(parallel=False)
        make("install", parallel=False)
