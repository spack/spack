from spack import *

class ExuberantCtags(Package):
    """The canonical ctags generator"""
    homepage = "ctags.sourceforge.net"
    url      = "http://downloads.sourceforge.net/project/ctags/ctags/5.8/ctags-5.8.tar.gz"

    version('5.8', 'c00f82ecdcc357434731913e5b48630d')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
