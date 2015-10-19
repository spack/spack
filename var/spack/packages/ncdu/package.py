from spack import *

class Ncdu(Package):
    """
    Ncdu is a disk usage analyzer with an ncurses interface. It is designed
    to find space hogs on a remote server where you don't have an entire
    gaphical setup available, but it is a useful tool even on regular desktop
    systems. Ncdu aims to be fast, simple and easy to use, and should be able
    to run in any minimal POSIX-like environment with ncurses installed.
    """

    homepage = "http://dev.yorhel.nl/ncdu"
    url      = "http://dev.yorhel.nl/download/ncdu-1.11.tar.gz"

    version('1.11', '9e44240a5356b029f05f0e70a63c4d12')
    version('1.10', '7535decc8d54eca811493e82d4bfab2d')
    version('1.9' , '93258079db897d28bb8890e2db89b1fb')
    version('1.8' , '94d7a821f8a0d7ba8ef3dd926226f7d5')
    version('1.7' , '172047c29d232724cc62e773e82e592a')

    depends_on("ncurses")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
            '--with-ncurses=%s' % spec['ncurses'])

        make()
        make("install")
