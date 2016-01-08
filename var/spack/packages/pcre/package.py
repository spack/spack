from spack import *

class Pcre(Package):
    """The PCRE package contains Perl Compatible Regular Expression
       libraries. These are useful for implementing regular expression
       pattern matching using the same syntax and semantics as Perl 5."""
    homepage = "http://www.pcre.org"""
    url      = "ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.36.tar.bz2"

    version('8.36', 'b767bc9af0c20bc9c1fe403b0d41ad97')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
