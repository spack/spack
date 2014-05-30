from spack import *

class Tmux(Package):
    """tmux is a terminal multiplexer. What is a terminal multiplexer? It lets
       you switch easily between several programs in one terminal, detach them (they
       keep running in the background) and reattach them to a different terminal. And
       do a lot more.
    """

    homepage = "http://tmux.sourceforge.net"
    url      = "http://downloads.sourceforge.net/project/tmux/tmux/tmux-1.9/tmux-1.9a.tar.gz"

    versions = { '1.9a' : 'b07601711f96f1d260b390513b509a2d', }

    depends_on('libevent')
    depends_on('ncurses')

    def install(self, spec, prefix):
        configure(
            "--prefix=%s" % prefix,
            "PKG_CONFIG_PATH=%s:%s" % (spec['libevent'].prefix, spec['ncurses'].prefix))

        make()
        make("install")
