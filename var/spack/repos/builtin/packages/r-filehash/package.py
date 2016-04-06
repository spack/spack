from spack import *

class RFilehash(Package):
    """Implements a simple key-value style database where character string keys are associated with data values that are stored on the disk. A simple interface is provided for inserting, retrieving, and deleting data from the database. Utilities are provided that allow 'filehash' databases to be treated much like environments and lists are already used in R. These utilities are provided to encourage interactive and exploratory analysis on large datasets. Three different file formats for representing the database are currently available and new formats can easily be incorporated by third parties for use in the 'filehash' framework."""

    homepage = 'https://cran.r-project.org/'
    url      = "https://cran.r-project.org/src/contrib/filehash_2.3.tar.gz"

    version('2.3', '01fffafe09b148ccadc9814c103bdc2f', expand=False)

    extends('R')

    def install(self, spec, prefix):
        R('CMD', 'INSTALL', '--library=%s' % self.module.r_lib_dir, '%s' % self.stage.archive_file)
