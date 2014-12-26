from spack import *

class GdkPixbuf(Package):
    """The Gdk Pixbuf is a toolkit for image loading and pixel buffer
       manipulation. It is used by GTK+ 2 and GTK+ 3 to load and
       manipulate images. In the past it was distributed as part of
       GTK+ 2 but it was split off into a separate package in
       preparation for the change to GTK+ 3."""
    homepage = "https://developer.gnome.org/gdk-pixbuf/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/gdk-pixbuf/2.31/gdk-pixbuf-2.31.1.tar.xz"

    version('2.31.2', '6be6bbc4f356d4b79ab4226860ab8523')

    depends_on("glib")
    depends_on("jpeg")
    depends_on("libpng")
    depends_on("libtiff")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
