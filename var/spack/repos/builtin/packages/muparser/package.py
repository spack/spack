from spack import *

class Muparser(Package):
    """C++ math expression parser library."""
    homepage = "http://muparser.beltoforion.de/"
    url      = "https://github.com/beltoforion/muparser/archive/v2.2.5.tar.gz"

    version('2.2.5', '02dae671aa5ad955fdcbcd3fee313fb7')

    def install(self, spec, prefix):
        options = ['--disable-debug',
                   '--disable-dependency-tracking',
                   '--prefix=%s' % prefix]

        configure(*options)

        make(parallel=False)
        make("install")
