from spack import *

class Openssl(Package):
    """The OpenSSL Project is a collaborative effort to develop a
       robust, commercial-grade, full-featured, and Open Source
       toolkit implementing the Secure Sockets Layer (SSL v2/v3) and
       Transport Layer Security (TLS v1) protocols as well as a
       full-strength general purpose cryptography library."""
    homepage = "http://www.openssl.org"
    url      = "http://www.openssl.org/source/openssl-1.0.1h.tar.gz"

    version('1.0.1h', '8d6d684a9430d5cc98a62a5d8fbda8cf')
    version('1.0.2d', '38dd619b2e77cbac69b99f52a053d25a')

    depends_on("zlib")
    parallel = False

    def install(self, spec, prefix):
        config = Executable("./config")
        config("--prefix=%s" % prefix,
               "--openssldir=%s/etc/openssl" % prefix,
               "zlib",
               "no-krb5",
               "shared")

        make()
        make("install")
