from spack import *

class Gtkplus(Package):
    """The GTK+ 2 package contains libraries used for creating graphical user interfaces for applications."""
    homepage = "http://www.gtk.org"

    version('2.24.25', '612350704dd3aacb95355a4981930c6f',
            url="http://ftp.gnome.org/pub/gnome/sources/gtk+/2.24/gtk+-2.24.25.tar.xz")

    depends_on("atk")
    depends_on("gdk-pixbuf")
    depends_on("pango")

    def patch(self):
        # remove disable deprecated flag.
        filter_file(r'CFLAGS="-DGDK_PIXBUF_DISABLE_DEPRECATED $CFLAGS"',
                    '', 'configure', string=True)

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
