from spack import *

class Intelmpi(Package):
    """Dummy package created, need to check if using module is sufficient enough! Mostly!"""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/intelmpi-1.0.tar.gz"

    version('5.0.1', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpiicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpiicpc'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpiifort'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpiifort'))

        spack_env.set('MPICH_CC', spack_cc)
        spack_env.set('MPICH_CXX', spack_cxx)
        spack_env.set('MPICH_F77', spack_f77)
        spack_env.set('MPICH_F90', spack_fc)
        spack_env.set('MPICH_FC', spack_fc)

    def setup_dependent_package(self, module, dep_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpiicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpiicpc')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpiifort')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpiifort')

    def install(self, spec, prefix):
        configure("--prefix=%s" % prefix)
        make()
        make("install")
