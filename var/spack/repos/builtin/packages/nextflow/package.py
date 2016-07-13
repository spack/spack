from spack import *
from glob import glob
import os

class Nextflow(Package):
    """Data-driven computational pipelines"""

    homepage = "http://www.nextflow.io"

    version('0.20.1', '0e4e0e3eca1c2c97f9b4bffd944b923a',
            url='https://github.com/nextflow-io/nextflow/releases/download/v0.20.1/nextflow',
            expand=False)

    depends_on('jdk')

    def unpack(self):
        pass

    def install(self, spec, prefix):
        chmod = which('chmod')

        mkdirp(prefix.bin)
        install("nextflow", join_path(prefix.bin, "nextflow"))
        chmod('+x', join_path(prefix.bin, "nextflow"))
