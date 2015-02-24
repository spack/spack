import os
from spack import *

class Mpibash(Package):
    """Parallel scripting right from the Bourne-Again Shell (Bash)"""
    homepage = "http://www.ccs3.lanl.gov/~pakin/software/mpibash-4.3.html"

    version('4.3', '81348932d5da294953e15d4814c74dd1',
            url="http://ftp.gnu.org/gnu/bash/bash-4.3.tar.gz")

    # patch -p1 < ../mpibash-4.3.patch
    patch('mpibash-4.3.patch', level=1, when='@4.3')

    # above patch modifies configure.ac
    depends_on('autoconf')

    # uses MPI_Exscan which is in MPI-1.2 and later
    depends_on('mpi@1.2:')

    depends_on('libcircle')

    def install(self, spec, prefix):
        # run autoconf to rebuild configure
        autoconf = which('autoconf')
        autoconf()

        configure("--prefix=" + prefix,
                  "CC=mpicc")

        make(parallel=False)

        make("install")
