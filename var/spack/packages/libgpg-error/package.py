from spack import *

class LibgpgError(Package):
    """Libgpg-error is a small library that defines common error
       values for all GnuPG components. Among these are GPG, GPGSM,
       GPGME, GPG-Agent, libgcrypt, Libksba, DirMngr, Pinentry,
       SmartCard Daemon and possibly more in the future. """

    homepage = "https://www.gnupg.org/related_software/libgpg-error"
    url      = "ftp://ftp.gnupg.org/gcrypt/libgpg-error/libgpg-error-1.18.tar.bz2"

    version('1.18', '12312802d2065774b787cbfc22cc04e9')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
