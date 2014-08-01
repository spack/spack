import os
from spack import *

class Dtcmp(Package):
    """The Datatype Comparison Library provides comparison operations and parallel sort algorithms for MPI applications."""

    homepage = "https://github.com/hpc/dtcmp"
    url      = "https://github.com/hpc/dtcmp/releases/download/v1.0.3/dtcmp-1.0.3.tar.gz"

    versions = { '1.0.3' : 'cdd8ccf71e8ff67de2558594a7fcd317' }
    #version('1.0.3', 'cdd8ccf71e8ff67de2558594a7fcd317')

    depends_on('mpi')
    depends_on('lwgrp')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix,
                  "--with-lwgrp=" + spec['lwgrp'].prefix)
        make()
        make("install")
