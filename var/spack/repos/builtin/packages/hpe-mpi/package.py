from spack import *

class HpeMpi(Package):
    """HPE-SGI MPI package"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/hpempi-1.0.tar.gz"

    version('2.16', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def do_fetch(self, mirror_only=False):
        raise RuntimeError('HPE MPI should be configured as external package')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        bindir = self.prefix.bin
        spack_env.set('MPICC',  join_path(bindir, 'mpicc'))
        spack_env.set('MPICXX', join_path(bindir, 'mpicxx'))
        spack_env.set('MPIF77', join_path(bindir, 'mpif77'))
        spack_env.set('MPIF90', join_path(bindir, 'mpif90'))

        spack_env.set('MPICC_CC', spack_cc)
        spack_env.set('MPICXX_CXX', spack_cxx)
        spack_env.set('MPIF90_F90', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        bindir = self.prefix.bin
        self.spec.mpicc = join_path(bindir, 'mpicc')
        self.spec.mpicxx = join_path(bindir, 'mpicxx')
        self.spec.mpifc = join_path(bindir, 'mpif77')
        self.spec.mpif77 = join_path(bindir, 'mpif90')
