from spack import *

class Postgresql(Package):
    """PostgreSQL is a powerful, open source object-relational
       database system. It has more than 15 years of active
       development and a proven architecture that has earned it a
       strong reputation for reliability, data integrity, and
       correctness."""
    homepage = "http://www.postgresql.org/"
    url      = "http://ftp.postgresql.org/pub/source/v9.3.4/postgresql-9.3.4.tar.bz2"

    version('9.3.4', 'd0a41f54c377b2d2fab4a003b0dac762')

    depends_on("openssl")

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix,
                  "--with-openssl")
        make()
        make("install")
