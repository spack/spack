from spack import *

class RMagic(Package):
    """A collection of efficient, vectorized algorithms for the creation and investigation of magic squares and hypercubes, including a variety of functions for the manipulation and analysis of arbitrarily dimensioned arrays."""
    homepage = "https://cran.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/magic_1.5-6.tar.gz"

    version('1.5-6', 'a68e5ced253b2196af842e1fc84fd029', expand=False)

    extends('R')

    depends_on('r-abind')

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library=%s' % self.module.r_lib_dir, '%s' % self.stage.archive_file)
