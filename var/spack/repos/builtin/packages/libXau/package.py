from spack import *


class Libxau(Package):
    """The libXau package contains a library implementing the X11 Authorization
    Protocol. This is useful for restricting client access to the display.i
    """

    homepage = "http://xorg.freedesktop.org"
    url      = "https://www.x.org/archive//individual/lib/libXau-1.0.8.tar.gz"

    version('1.0.8', 'a85cd601d82bc79c0daa280917572e20')
    version('1.0.7', '3ab7a4d1aac1b7f8ccc6b9755a19f252')
    version('1.0.6', 'ee1ee30c00d1e033cfc0237a349e1219')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
