from spack import *

class Sparsehash(Package):
    """Sparse and dense hash-tables for C++ by Google"""
    homepage = "https://github.com/sparsehash/sparsehash"
    url      = "https://github.com/sparsehash/sparsehash/archive/sparsehash-2.0.3.tar.gz"

    version('2.0.3', 'd8d5e2538c1c25577b3f066d7a55e99e')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
