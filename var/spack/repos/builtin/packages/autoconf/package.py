from spack import *

class Autoconf(Package):
    """Autoconf -- system configuration part of autotools"""
    homepage = "https://www.gnu.org/software/autoconf/"
    url      = "http://ftp.gnu.org/gnu/autoconf/autoconf-2.69.tar.gz"

    version('2.69', '82d05e03b93e45f5a39b828dc9c6c29b')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
