from spack import *

class Glib(Package):
    """The GLib package contains a low-level libraries useful for
       providing data structure handling for C, portability wrappers
       and interfaces for such runtime functionality as an event loop,
       threads, dynamic loading and an object system."""
    homepage = "https://developer.gnome.org/glib/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/glib/2.42/glib-2.42.1.tar.xz"

    version('2.42.1', '89c4119e50e767d3532158605ee9121a')

    depends_on("libffi")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
