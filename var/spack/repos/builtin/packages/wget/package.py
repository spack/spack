from spack import *

class Wget(Package):
    """GNU Wget is a free software package for retrieving files using
       HTTP, HTTPS and FTP, the most widely-used Internet protocols. It
       is a non-interactive commandline tool, so it may easily be called
       from scripts, cron jobs, terminals without X-Windows support,
       etc."""

    homepage = "http://www.gnu.org/software/wget/"
    url      = "http://ftp.gnu.org/gnu/wget/wget-1.16.tar.gz"

    version('1.17', 'c4c4727766f24ac716936275014a0536')
    version('1.16', '293a37977c41b5522f781d3a3a078426')

    depends_on("openssl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-ssl=openssl",
                  "OPENSSL_CFLAGS=-I%s" % spec['openssl'].prefix.include,
                  "OPENSSL_LIBS=-L%s -lssl -lcrypto -lz" % spec['openssl'].prefix.lib)
        make()
        make("install")
