import os
from spack import *

class Fileutils(Package):
    """FileUtils provides a suite of MPI-based tools to manage large files and datasets on parallel file systems."""

    homepage = "https://github.com/hpc/fileutils"
    url      = "https://github.com/hpc/fileutils/releases/download/v0.0.1-alpha.4/fileutils-0.0.1-alpha.4.tar.gz"

    versions = { '0.0.1-alpha.4' : 'a01dbe5a2e03f3c70c7a98ec0a2554e1' }

    force_url = True

    depends_on('mpi')
    depends_on('libcircle')
    depends_on('libarchive')
    depends_on('dtcmp')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-libdtcmp=" + spec['dtcmp'].prefix)
        make()
        make("install")
