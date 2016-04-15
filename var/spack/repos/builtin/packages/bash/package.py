from spack import *

class Bash(Package):
    """The GNU Project's Bourne Again SHell."""

    homepage = "https://www.gnu.org/software/bash/"
    url      = "ftp://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz"

    version('4.3', '81348932d5da294953e15d4814c74dd1')

    depends_on('readline')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--with-curses',
                  '--with-installed-readline=%s' % spec['readline'].prefix)

        make()
        make("tests")
        make("install")
