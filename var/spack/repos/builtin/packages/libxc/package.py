from spack import *

class Libxc(Package):
    """Libxc is a library of exchange-correlation functionals for
    density-functional theory."""

    homepage = "http://www.tddft.org/programs/octopus/wiki/index.php/Libxc"
    url      = "http://www.tddft.org/programs/octopus/down.php?file=libxc/libxc-2.2.2.tar.gz"

    version('2.2.2', 'd9f90a0d6e36df6c1312b6422280f2ec')


    def install(self, spec, prefix):
        configure('--prefix=%s' % prefix,
                  '--enable-shared')

        make()
        make("install")
