from spack import *

class Blitz(Package):
    """N-dimensional arrays for C++"""
    homepage = "http://github.com/blitzpp/blitz"
    url      = "https://github.com/blitzpp/blitz/tarball/1.0.0"

    version('1.0.0', '9f040b9827fe22228a892603671a77af')

    # No dependencies

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)
        make()
        make("install")
