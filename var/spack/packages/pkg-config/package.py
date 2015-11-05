from spack import *

class PkgConfig(Package):
    """pkg-config is a helper tool used when compiling applications and libraries"""
    homepage = "http://www.freedesktop.org/wiki/Software/pkg-config/"
    url      = "http://pkgconfig.freedesktop.org/releases/pkg-config-0.28.tar.gz"

    version('0.28', 'aa3c86e67551adc3ac865160e34a2a0d')

    parallel = False

    def install(self, spec, prefix):
        configure("--prefix=%s" %prefix, "--enable-shared")

        make()
        make("install")

