from spack import *

class Libffi(Package):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""
    homepage = "https://sourceware.org/libffi/"
    url      = "ftp://sourceware.org/pub/libffi/libffi-3.1.tar.gz"

    version('3.1', 'f5898b29bbfd70502831a212d9249d10')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
