import os
from spack import *

class Fileutils(Package):
    """FileUtils provides a suite of MPI-based tools to manage large files
       and datasets on parallel file systems."""

    homepage = "https://github.com/hpc/fileutils"
    url      = "https://github.com/hpc/fileutils/releases/download/v0.0.1-alpha.4/fileutils-0.0.1-alpha.4.tar.gz"

    version('0.0.1-alpha.4', 'e37b48ea43c95f5a1ede0ee01019ae58')

    depends_on('mpi')
    depends_on('libcircle')
    depends_on('libarchive')
    depends_on('dtcmp')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-dtcmp=" + spec['dtcmp'].prefix)
        make()
        make("install")
