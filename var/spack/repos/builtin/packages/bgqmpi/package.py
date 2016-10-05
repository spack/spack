from spack import *

class Bgqmpi(Package):
    """Dummy package for BG-Q MPI"""

    url      = "http://www.example.com/intelmpi-1.0.tar.gz"

    version('3.2')
    provides('mpi@:3.0')

    def get_compiler_specific_prefix(self, spec):
        prefix = spec.prefix

        if spec.satisfies('%xl'):
            prefix = join_path(spec.prefix, 'xl/bin')
        if spec.satisfies('%gcc'):
            prefix = join_path(spec.prefix, 'gcc/bin')

        return prefix

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        compiler_prefix = self.get_compiler_specific_prefix(self.spec)
        spack_env.set('MPICC',  join_path(compiler_prefix, 'mpicc'))
        spack_env.set('MPICXX', join_path(compiler_prefix, 'mpicxx'))
        spack_env.set('MPIF77', join_path(compiler_prefix, 'mpif77'))
        spack_env.set('MPIF90', join_path(compiler_prefix, 'mpif90'))

    def setup_dependent_package(self, module, dep_spec):
        compiler_prefix = self.get_compiler_specific_prefix(self.spec)
        self.spec.mpicc = join_path(compiler_prefix, 'mpicc')
        self.spec.mpicxx = join_path(compiler_prefix, 'mpicxx')
        self.spec.mpifc = join_path(compiler_prefix, 'mpif77')
        self.spec.mpif77 = join_path(compiler_prefix, 'mpif90')

