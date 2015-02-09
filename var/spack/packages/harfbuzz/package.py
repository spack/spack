from spack import *

class Harfbuzz(Package):
    """The Harfbuzz package contains an OpenType text shaping engine."""
    homepage = "http://www.freedesktop.org/wiki/Software/HarfBuzz/"
    url      = "http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-0.9.37.tar.bz2"

    version('0.9.37', 'bfe733250e34629a188d82e3b971bc1e')

    depends_on("glib")
    depends_on("icu")
    depends_on("freetype")

    def patch(self):
        change_sed_delimiter('@', ';', 'src/Makefile.in')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
