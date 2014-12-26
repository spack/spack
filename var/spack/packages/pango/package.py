from spack import *

class Pango(Package):
    """Pango is a library for laying out and rendering of text, with
       an emphasis on internationalization. It can be used anywhere
       that text layout is needed, though most of the work on Pango so
       far has been done in the context of the GTK+ widget toolkit."""
    homepage = "http://www.pango.org"
    url      = "http://ftp.gnome.org/pub/gnome/sources/pango/1.36/pango-1.36.8.tar.xz"

    version('1.36.8', '217a9a753006275215fa9fa127760ece')

    depends_on("harfbuzz")
    depends_on("cairo")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
