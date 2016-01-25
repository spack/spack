from spack import *

class Judy(Package):
    """A general-purpose dynamic array, associative array and hash-trie - Judy"""
    homepage = "http://judy.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/judy/judy/Judy-1.0.5/Judy-1.0.5.tar.gz"

    version('1.0.5', '115a0d26302676e962ae2f70ec484a54')
    parallel = False

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
