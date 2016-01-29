from spack import *

class M4(Package):
    """GNU M4 is an implementation of the traditional Unix macro processor."""
    homepage = "https://www.gnu.org/software/m4/m4.html"
    url      = "ftp://ftp.gnu.org/gnu/m4/m4-1.4.17.tar.gz"

    version('1.4.17', 'a5e9954b1dae036762f7b13673a2cf76')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
