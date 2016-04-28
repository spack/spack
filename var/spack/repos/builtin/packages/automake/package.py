from spack import *

class Automake(Package):
    """Automake -- make file builder part of autotools"""
    homepage = "http://www.gnu.org/software/automake/"
    url      = "http://ftp.gnu.org/gnu/automake/automake-1.14.tar.gz"

    version('1.15',   '716946a105ca228ab545fc37a70df3a3')
    version('1.14.1', 'd052a3e884631b9c7892f2efce542d75')
    version('1.11.6', '0286dc30295b62985ca51919202ecfcc')

    depends_on('autoconf')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
