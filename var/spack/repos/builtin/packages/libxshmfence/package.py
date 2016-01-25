from spack import *

class Libxshmfence(Package):
    """This is a tiny library that exposes a event API on top of Linux
    futexes."""

    homepage = "http://keithp.com/blogs/dri3_extension/" # not really...
    url      = "http://xorg.freedesktop.org/archive/individual/lib/libxshmfence-1.2.tar.gz"

    version('1.2', 'f0b30c0fc568b22ec524859ee28556f1')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)

        make()
        make("install")
