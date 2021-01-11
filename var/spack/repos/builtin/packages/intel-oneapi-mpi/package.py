# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import glob

from spack import *


releases = {
    '2021.1.1': {'irc_id': '17397', 'build': '76'}}


class IntelOneapiMpi(IntelOneApiLibraryPackage):
    """Intel oneAPI MPI."""

    maintainers = ['rscohn2']

    homepage = 'https://software.intel.com/content/www/us/en/develop/tools/oneapi/components/mpi-library.html'

    version('2021.1.1', sha256='8b7693a156c6fc6269637bef586a8fd3ea6610cac2aae4e7f48c1fbb601625fe', expand=False)

    provides('mpi@:3')

    def __init__(self, spec):
        self.component_info(dir_name='mpi',
                            components='intel.oneapi.lin.mpi.devel',
                            releases=releases,
                            url_name='mpi_oneapi')
        super(IntelOneapiMpi, self).__init__(spec)

    @property
    def libs(self):
        libs = []
        for dir in ['lib/release_mt', 'lib', 'libfabric/lib']:
            lib_path = '{0}/{1}/latest/{2}'.format(self.prefix, self._dir_name, dir)
            ldir = find_libraries('*', root=lib_path, shared=True, recursive=False)
            libs += ldir
        return libs

    def _join_prefix(self, path):
#        return join_path(self.prefix, 'compiler', 'latest', 'linux', path)
        return join_path(self.prefix, 'mpi', 'latest', path)

    def _ld_library_path(self):
        dirs = ['lib',
                'lib/release',
                'libfabric/lib']
        for dir in dirs:
            yield self._join_prefix(dir)


    def setup_run_environment(self, env):
        env.prepend_path('PATH', self._join_prefix('bin'))
        env.prepend_path('CPATH', self._join_prefix('include'))
        env.prepend_path('LIBRARY_PATH', self._join_prefix('lib'))
        for dir in self._ld_library_path():
            env.prepend_path('LD_LIBRARY_PATH', self._join_prefix(dir))

#prepend-path    LD_LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/lib
#prepend-path    LD_LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/lib/release
#prepend-path    LD_LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/libfabric/lib
#prepend-path    LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/lib
#prepend-path    LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/lib/release
#prepend-path    LIBRARY_PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/libfabric/lib
#prepend-path    PATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/bin
#prepend-path    CPATH /soft/spack/opt/spack/linux-opensuse_leap15-cascadelake/oneapi-2021.1/intel-oneapi-mpi-2021.1.1-yvh3tnaanbpcbpli7dollzw6ibaszye6/mpi/latest/include
