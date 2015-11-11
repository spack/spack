from spack import *

class Libpciaccess(Package):
    """Generic PCI access library"""
    homepage = "http://cgit.freedesktop.org/xorg/lib/libpciaccess/"
    url      = "http://pkgs.fedoraproject.org/repo/pkgs/libpciaccess/libpciaccess-0.13.2.tar.bz2/b7c0d3afce14eedca57312a3141ec13a/libpciaccess-0.13.2.tar.bz2"

    version('0.13.2', 'b7c0d3afce14eedca57312a3141ec13a')

    def install(self, spec, prefix):
        import os
        os.system("autoconf")
        configure('--prefix=%s' % prefix)

        make()
        make("install")
