import os
from spack import *

class Lwgrp(Package):
    """Thie light-weight group library provides process group representations using O(log N) space and time."""

    homepage = "https://github.com/hpc/lwgrp"
    url      = "https://github.com/hpc/lwgrp/releases/download/v1.0.2/lwgrp-1.0.2.tar.gz"

    versions = { '1.0.2' : 'ab7ba3bdd8534a651da5076f47f27d8a' }

    depends_on('mpi')

    def install(self, spec, prefix):
        configure("--prefix=" + prefix)
        make()
        make("install")
