import os
from spack import *

class Libcircle(Package):
    """libcircle provides an efficient distributed queue on a cluster,
       using self-stabilizing work stealing."""

    homepage = "https://github.com/hpc/libcircle"

    version('0.2.1-rc.1', '2b1369a5736457239f908abf88143ec2',
             url='https://github.com/hpc/libcircle/releases/download/0.2.1-rc.1/libcircle-0.2.1-rc.1.tar.gz')

    depends_on('mpi')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
