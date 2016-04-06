from spack import *

class RAbind(Package):
    """Combine multidimensional arrays into a single array. This is a generalization of 'cbind' and 'rbind'. Works with vectors, matrices, and higher-dimensional arrays. Also provides functions 'adrop', 'asub', and 'afill' for manipulating, extracting and replacing data in arrays."""

    homepage = "https://cran.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/abind_1.4-3.tar.gz"

    version('1.4-3', '10fcf80c677b991bf263d38be35a1fc5', expand=False)

    extends('R')

    def install(self, spec, prefix):

        R('CMD', 'INSTALL', '--library=%s' % self.module.r_lib_dir, '%s' % self.stage.archive_file)
