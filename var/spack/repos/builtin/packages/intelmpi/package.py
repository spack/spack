from spack import *

class Intelmpi(Package):
    """Intel MPI"""

    homepage = "http://www.example.com"
    url      = "https://software.intel.com/en-us/intel-mpi-library"

    version('4.1.0')

    # Provides a virtual dependency 'mpi'
    provides('mpi')

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

#    def install(self, spec, prefix):
#        configure("--prefix=%s" % prefix)
#        make()
#        make("install")
