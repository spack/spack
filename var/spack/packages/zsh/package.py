from spack import *

class Zsh(Package):
    """ The ZSH shell """
    homepage = "http://www.zsh.org"
    url      = "http://www.zsh.org/pub/zsh-5.0.8.tar.bz2"

    version('5.0.8', 'e6759e8dd7b714d624feffd0a73ba0fe')

    depends_on("pcre")

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
