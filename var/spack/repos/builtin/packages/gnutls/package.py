from spack import *

class Gnutls(Package):
    """GnuTLS is a secure communications library implementing the SSL,
       TLS and DTLS protocols and technologies around them. It
       provides a simple C language application programming interface
       (API) to access the secure communications protocols as well as
       APIs to parse and write X.509, PKCS #12, OpenPGP and other
       required structures. It is aimed to be portable and efficient
       with focus on security and interoperability."""

    homepage = "http://www.gnutls.org"
    url      = "ftp://ftp.gnutls.org/gcrypt/gnutls/v3.3/gnutls-3.3.9.tar.xz"

    version('3.3.9', 'ff61b77e39d09f1140ab5a9cf52c58b6')

    depends_on("nettle")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
