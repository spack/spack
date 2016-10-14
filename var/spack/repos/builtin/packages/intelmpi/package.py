from spack import *
import os
import re

from spack.pkg.builtin.intel import IntelInstaller, filter_pick, \
    get_all_components


class Intelmpi(IntelInstaller):
    """Intel MPI

    Note: You will have to add the download file to a
    mirror so that Spack can find it. For instructions on how to set up a
    mirror, see http://software.llnl.gov/spack/mirrors.html"""

    homepage = "https://software.intel.com/en-us/intel-mpi-library"

    # TODO: can also try the online installer (will download files on demand)
    version('5.1.1.109', 'aa4aaec41526aa5b244e531811877b01',
        url="file://%s/l_mpi_p_5.1.1.109.tgz" % os.getcwd())

    variant('all', default=True,
            description="Install all files with the requested edition")

    provides('mpi')

    def install(self, spec, prefix):

        if spec.satisfies('+all'):
            self.intel_components = 'ALL'
        
        IntelInstaller.install(self, spec, prefix)

    def setup_environment(self, spack_env, run_env):
        # TODO: Determine variables needed for the professional edition.

        major_ver = self.version[1]

        # Remove paths that were guessed but are incorrect for this package.
        run_env.remove_path('PATH',
                            join_path(self.prefix, 'bin'))
        run_env.remove_path('CMAKE_PREFIX_PATH',
                            self.prefix)

        # Only I_MPI_ROOT is set here because setting the various PATH
        # variables will potentially be in conflict with other MPI
        # environment modules. The I_MPI_ROOT environment variable can be
        # used as a base to set necessary PATH variables for using Intel
        # MPI. It is also possible to set the variables in the modules.yaml
        # file if Intel MPI is the dominant, or only, MPI on a system.
        run_env.set('I_MPI_ROOT', join_path(self.prefix, 'impi',
                                                self.version))

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('MPICC',  join_path(self.prefix.bin, 'mpicc'))
        spack_env.set('MPICXX', join_path(self.prefix.bin, 'mpicxx'))
        spack_env.set('MPIF77', join_path(self.prefix.bin, 'mpif77'))
        spack_env.set('MPIF90', join_path(self.prefix.bin, 'mpif90'))
        # NOTE: Need to find a better way of setting this compiler argument
        # which is only required when building packages with intelmpi.
        spack_env.set('CXXFLAGS', '-DMPICH_IGNORE_CXX_SEEK')

    def setup_dependent_package(self, module, dep_spec):
        self.spec.mpicc = join_path(self.prefix.bin, 'mpicc')
        self.spec.mpicxx = join_path(self.prefix.bin, 'mpicxx')
        self.spec.mpifc = join_path(self.prefix.bin, 'mpif90')
        self.spec.mpif77 = join_path(self.prefix.bin, 'mpif77')

