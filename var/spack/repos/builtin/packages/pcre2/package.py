from spack import *

class Pcre2(Package):
    """The PCRE2 package contains Perl Compatible Regular Expression
       libraries. These are useful for implementing regular expression
       pattern matching using the same syntax and semantics as Perl 5."""
    homepage = "http://www.pcre.org"""
    url      = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre2-10.20.tar.bz2"

    version('10.20', 'dcd027c57ecfdc8a6c3af9d0acf5e3f7')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
