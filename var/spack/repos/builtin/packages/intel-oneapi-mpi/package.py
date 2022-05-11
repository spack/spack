# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


import platform

from spack.util.package import *


class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel oneAPI MPI."""

    maintainers = ['rscohn2', ]

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html'

    if platform.system() == 'Linux':
        version('2021.5.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18471/l_mpi_oneapi_p_2021.5.1.515_offline.sh',
                sha256='b992573959e39752e503e691564a0d876b099547c38b322d5775c5b06ec07a7f',
                expand=False)
        version('2021.5.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18370/l_mpi_oneapi_p_2021.5.0.495_offline.sh',
                sha256='3aae53fe77f7c6aac7a32b299c25d6ca9a00ba4e2d512a26edd90811e59e7471',
                expand=False)
        version('2021.4.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/18186/l_mpi_oneapi_p_2021.4.0.441_offline.sh',
                sha256='cc4b7072c61d0bd02b1c431b22d2ea3b84b967b59d2e587e77a9e7b2c24f2a29',
                expand=False)
        version('2021.3.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17947/l_mpi_oneapi_p_2021.3.0.294_offline.sh',
                sha256='04c48f864ee4c723b1b4ca62f2bea8c04d5d7e3de19171fd62b17868bc79bc36',
                expand=False)
        version('2021.2.0',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17729/l_mpi_oneapi_p_2021.2.0.215_offline.sh',
                sha256='d0d4cdd11edaff2e7285e38f537defccff38e37a3067c02f4af43a3629ad4aa3',
                expand=False)
        version('2021.1.1',
                url='https://registrationcenter-download.intel.com/akdlm/irc_nas/17397/l_mpi_oneapi_p_2021.1.1.76_offline.sh',
                sha256='8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe',
                expand=False)

    variant('ilp64', default=False,
            description='Build with ILP64 support')
    variant('external-libfabric', default=False, description='Enable external libfabric dependency')
    depends_on('libfabric', when='+external-libfabric', type=('link', 'run'))

    provides('mpi@:3.1')

    @property
    def component_dir(self):
        return 'mpi'

    def setup_dependent_package(self, module, dep_spec):
        dir = join_path(self.component_path, 'bin')
        self.spec.mpicc  = join_path(dir, 'mpicc')
        self.spec.mpicxx = join_path(dir, 'mpicxx')
        self.spec.mpif77 = join_path(dir, 'mpif77')
        self.spec.mpifc  = join_path(dir, 'mpifc')

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('MPICH_CC', spack_cc)
        env.set('MPICH_CXX', spack_cxx)
        env.set('MPICH_F77', spack_f77)
        env.set('MPICH_F90', spack_fc)
        env.set('MPICH_FC', spack_fc)

        # Set compiler wrappers for dependent build stage
        dir = join_path(self.component_path, 'bin')
        env.set('MPICC', join_path(dir, 'mpicc'))
        env.set('MPICXX', join_path(dir, 'mpicxx'))
        env.set('MPIF77', join_path(dir, 'mpif77'))
        env.set('MPIF90', join_path(dir, 'mpif90'))
        env.set('MPIFC', join_path(dir, 'mpifc'))

        env.set('I_MPI_ROOT', self.component_path)

    @property
    def headers(self):
        include_path = join_path(self.component_path, 'include')
        headers = find_headers('*', include_path)
        if '+ilp64' in self.spec:
            headers += find_headers('*', join_path(include_path, 'ilp64'))
        return headers

    @property
    def libs(self):
        lib_dir = join_path(self.component_path, 'lib')
        release_lib_dir = join_path(lib_dir, 'release')
        libs = []
        if '+ilp64' in self.spec:
            libs += find_libraries('libmpi_ilp64', release_lib_dir)
        libs += find_libraries(['libmpicxx', 'libmpifort'], lib_dir)
        libs += find_libraries('libmpi', release_lib_dir)
        libs += find_system_libraries(['libdl', 'librt', 'libpthread'])

        # Find libfabric for libmpi.so
        if '+external-libfabric' in self.spec:
            libs += self.spec['libfabric'].libs
        else:
            libs += find_libraries(['libfabric'],
                                   join_path(self.component_path, 'libfabric', 'lib'))

        return libs

    def install(self, spec, prefix):
        super(IntelOneapiMpi, self).install(spec, prefix)

        # When spack builds from source
        # fix I_MPI_SUBSTITUTE_INSTALLDIR and
        #   __EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__
        scripts = ["mpif77", "mpif90", "mpigcc", "mpigxx", "mpiicc", "mpiicpc",
                   "mpiifort"]
        for script in scripts:
            file = join_path(self.component_path, 'bin', script)
            filter_file('I_MPI_SUBSTITUTE_INSTALLDIR',
                        self.component_path, file, backup=False)
            filter_file('__EXEC_PREFIX_TO_BE_FILLED_AT_INSTALL_TIME__',
                        self.component_path, file, backup=False)
