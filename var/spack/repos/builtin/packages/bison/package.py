from spack import *

class Bison(Package):
    """Bison is a general-purpose parser generator that converts 
    an annotated context-free grammar into a deterministic LR or 
    generalized LR (GLR) parser employing LALR(1) parser tables."""

    homepage = "http://www.gnu.org/software/bison/"
    url      = "http://ftp.gnu.org/gnu/bison/bison-3.0.tar.gz"

    version('3.0.4', 'a586e11cd4aff49c3ff6d3b6a4c9ccf8')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
