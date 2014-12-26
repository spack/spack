from spack import *

class Xz(Package):
    """XZ Utils is free general-purpose data compression software with
       high compression ratio. XZ Utils were written for POSIX-like
       systems, but also work on some not-so-POSIX systems. XZ Utils are
       the successor to LZMA Utils."""
    homepage = "http://tukaani.org/xz/"
    url      = "http://tukaani.org/xz/xz-5.2.0.tar.bz2"

    version('5.2.0', '867cc8611760240ebf3440bd6e170bb9')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
