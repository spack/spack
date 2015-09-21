from spack import *

class Ncurses(Package):
    """The ncurses (new curses) library is a free software emulation of curses
       in System V Release 4.0, and more. It uses terminfo format, supports pads and
       color and multiple highlights and forms characters and function-key mapping,
       and has all the other SYSV-curses enhancements over BSD curses.
    """

    homepage = "http://invisible-island.net/ncurses/ncurses.html"

    version('5.9', '8cb9c412e5f2d96bc6f459aa8c6282a1',
            url='http://ftp.gnu.org/pub/gnu/ncurses/ncurses-5.9.tar.gz')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-shared",
                  "--enable-widec",
                  "--disable-pc-files",
                  "--without-ada")
        make()
        make("install")

        configure("--prefix=%s" % prefix,
                  "--with-shared",
                  "--disable-widec",
                  "--disable-pc-files",
                  "--without-ada")
        make()
        make("install")

