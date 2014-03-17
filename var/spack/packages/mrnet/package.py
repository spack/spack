from spack import *

class Mrnet(Package):
    """The MRNet Multi-Cast Reduction Network."""
    homepage = "http://paradyn.org/mrnet"
    url      = "ftp://ftp.cs.wisc.edu/paradyn/mrnet/mrnet_4.0.0.tar.gz"

    versions = { '4.0.0' : 'd00301c078cba57ef68613be32ceea2f', }
    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

        # TODO: copy configuration header files to include directory
        #       this can be removed once we have STAT-2.1.0
        import shutil
        shutil.copy2('%s/lib/mrnet-%s/include/mrnet_config.h' % (prefix, self.version), '%s/include/mrnet_config.h' % prefix)
        shutil.copy2('%s/lib/xplat-%s/include/xplat_config.h' % (prefix, self.version), '%s/include/xplat_config.h' % prefix)
