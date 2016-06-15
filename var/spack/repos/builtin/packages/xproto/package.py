from spack import *


class Xproto(Package):
    """ X11 core wire protocol and auxiliary headers """
    homepage = "http://xorg.freedesktop.org"
    url      = \
        "https://www.x.org/archive//individual/proto/xproto-7.0.28.tar.gz"

    version('7.0.28', '0b42843b99aee3e4f6a9cc7710143f86')

    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix)

        make()
        make("install")
