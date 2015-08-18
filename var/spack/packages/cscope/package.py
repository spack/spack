from spack import *

class Cscope(Package):
    """Cscope is a developer's tool for browsing source code."""
    homepage = "http://http://cscope.sourceforge.net/"
    url      = "http://downloads.sourceforge.net/project/cscope/cscope/15.8b/cscope-15.8b.tar.gz"

    version('15.8b', '8f9409a238ee313a96f9f87fe0f3b176')

    # Can be configured to use flex (not necessary)
    # ./configure --with-flex

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
