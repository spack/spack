from spack import *
import os

class UtilLinux(Package):
    """Util-linux is a suite of essential utilities for any Linux system."""

    homepage = "http://freecode.com/projects/util-linux"
    url      = "https://www.kernel.org/pub/linux/utils/util-linux/v2.25/util-linux-2.25.tar.gz"

    version('2.25', 'f6d7fc6952ec69c4dc62c8d7c59c1d57')

    depends_on("python@2.7:")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix, 
                "PKG_CONFIG_PATH=%s/pkgconfig" % spec['python'].prefix.lib,
                "--disable-use-tty-group")

        make()
        make("install")
