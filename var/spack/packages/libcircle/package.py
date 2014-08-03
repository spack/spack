import os
from spack import *

class Libcircle(Package):
    """libcircle provides an efficient distributed queue on a cluster,
       using self-stabilizing work stealing."""

    homepage = "https://github.com/hpc/libcircle"
    url      = "https://github.com/adammoody/libcircle/releases/download/v0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz"

    version('0.2.1-rc.1', 'a10a14e76ac2ad7357a4b21b794e8e4e')

    depends_on('mpi')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
