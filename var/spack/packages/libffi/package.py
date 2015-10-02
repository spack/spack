from spack import *

class Libffi(Package):
    """The libffi library provides a portable, high level programming
    interface to various calling conventions. This allows a programmer
    to call any function specified by a call interface description at
    run time."""
    homepage = "https://sourceware.org/libffi/"
    
    version('3.2.1','83b89587607e3eb65c70d361f13bab43',url = "ftp://sourceware.org/pub/libffi/libffi-3.2.1.tar.gz")
    #version('3.1', 'f5898b29bbfd70502831a212d9249d10',url = "ftp://sourceware.org/pub/libffi/libffi-3.1.tar.gz") # Has a bug $(lib64) instead of ${lib64} in libffi.pc

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")

