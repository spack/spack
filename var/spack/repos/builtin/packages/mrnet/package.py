from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_5.0.1.tar.gz"
    list_url = "http://ftp.cs.wisc.edu/paradyn/mrnet"

    version('5.0.1', '17f65738cf1b9f9b95647ff85f69ecdd')
    version('4.1.0', '5a248298b395b329e2371bf25366115c')
    version('4.0.0', 'd00301c078cba57ef68613be32ceea2f')

    # Add a patch that brings mrnet-5.0.1 up to date with the current development tree
    # The development tree contains fixes needed for the krell based tools
    variant('krellpatch', default=False, description="Build MRNet with krell openspeedshop based patch.")
    patch('krell-5.0.1.patch', when='@5.0.1+krellpatch')



    variant('lwthreads', default=False, description="Also build the MRNet LW threadsafe libraries")
    parallel = False

    #depends_on("boost")
    depends_on("boost@1.53.0")

    def install(self, spec, prefix):
        # Build the MRNet LW thread safe libraries when the krelloptions variant is present
        if '+lwthreads' in spec:
           configure("--prefix=%s" %prefix, "--enable-shared", "--enable-ltwt-threadsafe")
        else:
           configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

