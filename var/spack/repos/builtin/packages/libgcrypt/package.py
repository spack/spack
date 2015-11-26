from spack import *

class Libgcrypt(Package):
    """Libgcrypt is a general purpose cryptographic library based on
       the code from GnuPG. It provides functions for all cryptographic
       building blocks: symmetric ciphers, hash algorithms, MACs, public
       key algorithms, large integer functions, random numbers and a lot
       of supporting functions. """
    homepage = "http://www.gnu.org/software/libgcrypt/"
    url      = "ftp://ftp.gnupg.org/gcrypt/libgcrypt/libgcrypt-1.6.2.tar.bz2"

    version('1.6.2', 'b54395a93cb1e57619943c082da09d5f')

    depends_on("libgpg-error")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
