from spack import *

class Automake(Package):
    """Automake -- make file builder part of autotools"""
    homepage = "http://www.gnu.org/software/automake/"
    url      = "http://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz"

    version('1.14.1', 'd052a3e884631b9c7892f2efce542d75')

    depends_on('autoconf')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
