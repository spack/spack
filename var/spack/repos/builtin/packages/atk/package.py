from spack import *

class Atk(Package):
    """ATK provides the set of accessibility interfaces that are
       implemented by other toolkits and applications. Using the ATK
       interfaces, accessibility tools have full access to view and
       control running applications."""
    homepage = "https://developer.gnome.org/atk/"
    url      = "http://ftp.gnome.org/pub/gnome/sources/atk/2.14/atk-2.14.0.tar.xz"

    version('2.14.0', 'ecb7ca8469a5650581b1227d78051b8b')

    depends_on("glib")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
