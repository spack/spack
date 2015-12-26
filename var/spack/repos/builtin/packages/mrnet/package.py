from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_4.0.0.tar.gz"

    version('4.0.0', 'd00301c078cba57ef68613be32ceea2f')
    version('4.1.0', '5a248298b395b329e2371bf25366115c')
    version('5.0.1', '17f65738cf1b9f9b95647ff85f69ecdd')

    variant('lwthreads', default=False, description="Also build the MRNet LW threadsafe libraries")
    parallel = False

    depends_on("boost")

    def install(self, spec, prefix):
        # Build the MRNet LW thread safe libraries when the krelloptions variant is present
        if '+lwthreads' in spec:
           configure("--prefix=%s" %prefix, "--enable-shared", "--enable-ltwt-threadsafe")
        else:
           configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

