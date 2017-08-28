from spack import *
import os

class Intelmpi(Package):
    """Dummy package created, need to check if using module is sufficient enough! Mostly!"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/intelmpi-1.0.tar.gz"

    version('develop', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def get_bin_dir(self):
        if os.path.isdir(self.prefix.bin):
            bindir = self.prefix.bin
        elif os.path.isdir(self.prefix.bin64):
            bindir = self.prefix.bin64
        else:
            raise RuntimeError('No suitable Intel MPI bindir found')
        return bindir

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        bindir = self.get_bin_dir()
        spack_env.set('MPICC',  join_path(bindir, 'mpiicc'))
        spack_env.set('MPICXX', join_path(bindir, 'mpiicpc'))
        spack_env.set('MPIF77', join_path(bindir, 'mpiifort'))
        spack_env.set('MPIF90', join_path(bindir, 'mpiifort'))

        spack_env.set('MPICH_CC', spack_cc)
        spack_env.set('MPICH_CXX', spack_cxx)
        spack_env.set('MPICH_F77', spack_f77)
        spack_env.set('MPICH_F90', spack_fc)
        spack_env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        bindir = self.get_bin_dir()

        self.spec.mpicc = join_path(bindir, 'mpiicc')
        self.spec.mpicxx = join_path(bindir, 'mpiicpc')
        self.spec.mpifc = join_path(bindir, 'mpiifort')
        self.spec.mpif77 = join_path(bindir, 'mpiifort')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
