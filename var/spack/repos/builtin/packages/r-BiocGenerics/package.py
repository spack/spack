from spack import *

class RBiocgenerics(Package):
    """S4 generic functions needed by many Bioconductor packages."""

    homepage = 'https://www.bioconductor.org/packages/release/bioc/html/BiocGenerics.html'
    url      = "https://www.bioconductor.org/packages/release/bioc/src/contrib/BiocGenerics_0.16.1.tar.gz"

    version('0.16.1', 'c2148ffd86fc6f1f819c7f68eb2c744f', expand=False)

    extends('R')

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library=%s' % self.module.r_lib_dir, '%s' % self.stage.archive_file)
