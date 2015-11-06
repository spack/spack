from spack import *


class Matio(Package):
    """matio is an C library for reading and writing Matlab MAT files"""
    homepage = "http://sourceforge.net/projects/matio/"
    url = "http://downloads.sourceforge.net/project/matio/matio/1.5.2/matio-1.5.2.tar.gz"

    version('1.5.2', '85b007b99916c63791f28398f6a4c6f1')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
