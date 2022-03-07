# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class LibsonataReport(CMakePackage):
    """
    `libsonatareport` provides C++ API for writing SONATA reports

    See also:
    https://github.com/AllenInstitute/sonata/blob/master/docs/SONATA_DEVELOPER_GUIDE.md
    """
    homepage = "https://github.com/BlueBrain/libsonatareport"
    git = "https://github.com/BlueBrain/libsonatareport.git"

    version('develop', branch='master', submodules=False, get_full_repo=True)
    version('1.1', tag='1.1', submodules=False)
    version('1.0.0.20220218', commit='905641', submodules=False)
    version('1.0.0.20211007', commit='b881fa', submodules=False)
    version('1.0.0.20210610', commit='ad8870', submodules=False)
    version('1.0.0.20210531', commit='f6916a', submodules=False)
    version('1.0', tag='1.0', submodules=False)
    version('0.1b', tag='0.1b', submodules=False)
    version('0.1a', tag='0.1a', submodules=False)

    variant('mpi', default=True, description="Enable MPI backend")

    depends_on('cmake@3.3:', type='build')
    depends_on('mpi', when='+mpi')
    depends_on('spdlog')
    depends_on('hdf5 ~mpi', when='~mpi')
    depends_on('hdf5 +mpi', when='+mpi')

    def cmake_args(self):
        result = [
            '-DSONATA_REPORT_ENABLE_SUBMODULES=OFF',
            '-DSONATA_REPORT_ENABLE_TEST=OFF',
            '-DSONATA_REPORT_ENABLE_WARNING_AS_ERROR=OFF',
        ]
        if self.spec.satisfies('+mpi'):
            result.append('-DSONATA_REPORT_ENABLE_MPI=ON')
        return result

    @property
    def libs(self):
        """Export the libsonata library.
        Sample usage: spec['libsonata'].libs.ld_flags
        """
        search_paths = [[self.prefix.lib64, False], [self.prefix.lib, False]]
        for path, recursive in search_paths:
            libs = find_libraries(['libsonatareport'], root=path,
                                  shared=True, recursive=False)
            if libs:
                return libs
        return None
