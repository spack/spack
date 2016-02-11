from spack import *

class Readline(Package):
    """The GNU Readline library provides a set of functions for use by
       applications that allow users to edit command li nes as they
       are typed in. Both Emacs and vi editing modes are
       available. The Readline library includes additional functions
       to maintain a list of previously-entered command lines, to
       recall and perhaps reedit those lines, and perform csh-like
       history expansion on previous commands. """
    homepage = "http://cnswww.cns.cwru.edu/php/chet/readline/rltop.html"
    url      = "ftp://ftp.cwru.edu/pub/bash/readline-6.3.tar.gz"

    version('6.3', '33c8fb279e981274f485fd91da77e94a')

    depends_on("ncurses")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make("SHLIB_LIBS=-lncurses")
        make("install")
