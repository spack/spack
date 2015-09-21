from spack import *

class Nettle(Package):
    """The Nettle package contains the low-level cryptographic library
    that is designed to fit easily in many contexts."""

    homepage = "http://www.example.com"
    url      = "http://ftp.gnu.org/gnu/nettle/nettle-2.7.1.tar.gz"

    version('2.7', '2caa1bd667c35db71becb93c5d89737f')

    depends_on('gmp')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
