from spack import *

class Isl(Package):
    """isl is a thread-safe C library for manipulating sets and
    relations of integer points bounded by affine constraints."""
    homepage = "http://isl.gforge.inria.fr"
    url      = "http://isl.gforge.inria.fr/isl-0.14.tar.bz2"

    version('0.14', 'acd347243fca5609e3df37dba47fd0bb')

    depends_on("gmp")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-gmp-prefix=%s" % spec['gmp'].prefix)
        make()
        make("install")
