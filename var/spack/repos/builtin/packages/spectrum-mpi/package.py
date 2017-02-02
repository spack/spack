from spack import *

class Spectrum(Package):
    """IBM MPI implementation from Spectrum MPI."""

    homepage = "http://www.example.com"
    url      = "http://www.example.com/ibm-mpi-10.1.0.tar.gz"

    version('10.1.0.2', '0123456789abcdef0123456789abcdef')
    version('10.1.0', '0123456789abcdef0123456789abcdef')

    provides('mpi')

    def install(self, spec, prefix):
        raise InstallError('IBM MPI is not installable; it is vendor supplied')

    def setup_dependent_package(self, module, dspec):
        # get library name and directory
        self.spec.mpi_base_dir = self.prefix
        self.spec.mpi_library = join_path(self.prefix.lib, 'libmpi_ibm.so')
        self.spec.mpi_include_path = self.prefix.include
        self.spec.mpi_library_path = self.prefix.lib
        self.spec.mpi_exec = join_path(self.prefix.bin, 'mpirun')
        self.spec.mpi_np_flag = '-np'
        if '%xl' in dspec or '%xl_r' in dspec:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpixlc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpixlC')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpixlf')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpixlf')
        else:
            self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
            self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
            self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')
            self.spec.mpif90 = join_path(self.prefix.bin, 'mpif90')
            self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')


    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        if '%xl' in dependent_spec or '%xl_r' in dependent_spec:
            spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpixlc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpixlC'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpixlf'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpixlf'))
        else:
            spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
            spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpic++'))
            spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
            spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))

        spack_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        run_env.prepend_path('LD_LIBRARY_PATH', self.prefix.lib)
        spack_env.set('OMPI_LDFLAGS', dependent_spec.package.rpath_args)
        spack_env.set('OMPI_CC', spack_cc)
        spack_env.set('OMPI_CXX', spack_cxx)
        spack_env.set('OMPI_FC', spack_fc)
        spack_env.set('OMPI_F77', spack_f77)
