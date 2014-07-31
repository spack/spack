from spack import *

class Mvapich2(Package):
    """mvapich2 is an MPI implmenetation for infiniband networks."""
    homepage = "http://mvapich.cse.ohio-state.edu/"

    version('1.9', '5dc58ed08fd3142c260b70fe297e127c',
            url="http://mvapich.cse.ohio-state.edu/download/mvapich2/mv2/mvapich2-1.9.tgz")
    version('2.0', '9fbb68a4111a8b6338e476dc657388b4',
            url='http://mvapich.cse.ohio-state.edu/download/mvapich/mv2/mvapich2-2.0.tar.gz')

    provides('mpi@:1', when='@1.9:')

    def install(self, spec, prefix):
        configure(
            "--prefix=" + prefix,
            "--enable-f77", "--enable-fc", "--enable-cxx",
            "--enable-fast=all", "--enable-g=dbg", "--enable-nmpi-as-mpi",
            "--enable-shared", "--enable-sharedlibs=gcc",
            "--enable-debuginfo",
            "--with-pm=no", "--with-pmi=slurm",
            "--with-device=ch3:psm",
            "--enable-romio", "--with-file-system=lustre+nfs+ufs",
            "--disable-mpe", "--without-mpe")
        make()
        make("install")
