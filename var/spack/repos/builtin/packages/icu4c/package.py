from spack import *

class Icu4c(Package):
    """ICU is a mature, widely used set of C/C++ and Java libraries 
    providing Unicode and Globalization support for software applications."""

    homepage = "http://site.icu-project.org/"
    url      = "http://downloads.sourceforge.net/project/icu/ICU4C/54.1/icu4c-54_1-src.tgz"

    version('54_1', 'e844caed8f2ca24c088505b0d6271bc0')

    def install(self, spec, prefix):
        cd("source")
        configure("--prefix=%s" % prefix)

        make()
        make("install")
