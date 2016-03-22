from spack import *

class Udunits2(Package):
    """Automated units conversion"""

    homepage = "http://www.unidata.ucar.edu/software/udunits"
    url      = "ftp://ftp.unidata.ucar.edu/pub/udunits/udunits-2.2.20.tar.gz"

    version('2.2.20', '1586b70a49dfe05da5fcc29ef239dce0')

    depends_on('expat')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
