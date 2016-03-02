from spack import *
import os.path

class Libpciaccess(Package):
    """Generic PCI access library."""

    homepage = "http://cgit.freedesktop.org/xorg/lib/libpciaccess/"
    url      = "http://xorg.freedesktop.org/archive/individual/lib/libpciaccess-0.13.4.tar.bz2"

    version('0.13.4', 'ace78aec799b1cf6dfaea55d3879ed9f')

    depends_on('libtool')

    def install(self, spec, prefix):
        # libpciaccess does not support OS X or PGI compilers
        if spec.satisfies('=darwin-x86_64') or spec.satisfies('%pgi'):
            # create a dummy directory
            mkdir(prefix.lib)
            return

        configure("--prefix=%s" % prefix)
        make()
        make("install")
