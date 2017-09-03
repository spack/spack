from spack import *


class Craympi(Package):
    """Dummy package for Cray MPI"""

    url      = "http://www.example.com/craympi-1.0.tar.gz"
    homepage = "http://www.example.com/craympi-1.0.tar.gz"

    version('3.2')
    provides('mpi@:3.0')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  spack_cc)
        spack_env.set('MPICXX', spack_cxx)
        spack_env.set('MPIF77', spack_f77)
        spack_env.set('MPIF90', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        self.spec.mpicc  = spack_cc
        self.spec.mpicxx = spack_cxx
        self.spec.mpif77 = spack_f77
        self.spec.mpifc  = spack_fc

