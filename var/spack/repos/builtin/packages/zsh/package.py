from spack import *

class Zsh(Package):
    """
    Zsh is a shell designed for interactive use, although it is also a powerful
    scripting language. Many of the useful features of bash, ksh, and tcsh were
    incorporated into zsh; many original features were added.
    """
    homepage = "http://www.zsh.org"
    url = "http://downloads.sourceforge.net/project/zsh/zsh/5.1.1/zsh-5.1.1.tar.gz"

    version('5.1.1', checksum='8ba28a9ef82e40c3a271602f18343b2f')

    depends_on("pcre")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
