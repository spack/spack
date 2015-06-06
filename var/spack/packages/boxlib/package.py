from spack import *

class Boxlib(Package):
    """BoxLib, a software framework for massively parallel
       block-structured adaptive mesh refinement (AMR) codes."""

    homepage = "https://ccse.lbl.gov/BoxLib/"
    url = "https://ccse.lbl.gov/pub/Downloads/BoxLib.git";

    # TODO: figure out how best to version this.  No tags in the repo!
    version('master', git='https://ccse.lbl.gov/pub/Downloads/BoxLib.git')

    depends_on('mpi')

    def install(self, spec, prefix):
        args = std_cmake_args
        args += ['-DCCSE_ENABLE_MPI=1',
                 '-DCMAKE_C_COMPILER=%s' % which('mpicc'),
                 '-DCMAKE_CXX_COMPILER=%s' % which('mpicxx'),
                 '-DCMAKE_Fortran_COMPILER=%s' % which('mpif90')]

        cmake('.', *args)
        make()
        make("install")

