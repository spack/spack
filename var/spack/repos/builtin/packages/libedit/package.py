from spack import *

class Libedit(Package):
    """An autotools compatible port of the NetBSD editline library"""
    homepage = "http://thrysoee.dk/editline/"
    url      = "http://thrysoee.dk/editline/libedit-20150325-3.1.tar.gz"

    version('3.1', '43cdb5df3061d78b5e9d59109871b4f6', url="http://thrysoee.dk/editline/libedit-20150325-3.1.tar.gz")

    depends_on('ncurses')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
