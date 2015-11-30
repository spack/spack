from spack import *

class Wget(Package):
    """GNU Wget is a free software package for retrieving files using
       HTTP, HTTPS and FTP, the most widely-used Internet protocols. It
       is a non-interactive commandline tool, so it may easily be called
       from scripts, cron jobs, terminals without X-Windows support,
       etc."""

    homepage = "http://www.gnu.org/software/wget/"
    url      = "http://ftp.gnu.org/gnu/wget/wget-1.16.tar.xz"

    version('1.16', 'fe102975ab3a6c049777883f1bb9ad07')

    depends_on("openssl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-ssl=openssl")
        make()
        make("install")
