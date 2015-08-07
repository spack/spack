from spack import *

class Libpciaccess(Package):
    """Generic PCI access library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libpciaccess/"
    url      = "http://cgit.freedesktop.org/xorg/lib/libpciaccess/"

    version('0.13.4', git='http://anongit.freedesktop.org/git/xorg/lib/libpciaccess.git',
            tag='libpciaccess-0.13.4')

    depends_on('autoconf')
    depends_on('libtool')

    def install(self, spec, prefix):
        from subprocess import call
        call(["./autogen.sh"])
        configure("--prefix=%s" % prefix)

        make()
        make("install")
