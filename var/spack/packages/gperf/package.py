from spack import *

class Gperf(Package):
    """GNU gperf is a perfect hash function generator. For a given
    list of strings, it produces a hash function and hash table, in
    form of C or C++ code, for looking up a value depending on the
    input string. The hash function is perfect, which means that the
    hash table has no collisions, and the hash table lookup needs a
    single string comparison only."""

    homepage = "https://www.gnu.org/software/gperf/"
    url      = "http://ftp.gnu.org/pub/gnu/gperf/gperf-3.0.4.tar.gz"

    version('3.0.4', 'c1f1db32fb6598d6a93e6e88796a8632')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
