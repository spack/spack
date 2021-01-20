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
    homepage = "https://github.com/BlueBrain/libsonata"
    git = "https://github.com/BlueBrain/libsonata.git"

    version('0.1.5', commit='55567360dab0e8', submodules=True, get_full_repo=True)
    version('0.1.4', commit='3881a52ad7fe8b', submodules=True, get_full_repo=True)
    version('develop', branch='master', submodules=False, get_full_repo=True)

    variant('mpi', default=True, description="Enable MPI backend")

    depends_on('cmake@3.3:', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('catch2')
    depends_on('fmt@4.0:')
    depends_on('highfive+mpi', when='+mpi')
    depends_on('highfive~mpi', when='~mpi')
    depends_on('mpi', when='+mpi')
    depends_on('spdlog')

    def cmake_args(self):
        result = [
            '-DEXTLIB_FROM_SUBMODULES=ON',
            '-DREPORTS_ONLY=ON',
            '-DCMAKE_CXX_FLAGS=-DFMT_HEADER_ONLY=1'
        ]
        if self.spec.satisfies('+mpi'):
            result.extend([
                '-DCMAKE_C_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicc
                ),
                '-DCMAKE_CXX_COMPILER:STRING={0}'.format(
                    self.spec['mpi'].mpicxx
                ),
                '-DREPORTS_ENABLE_MPI=ON',
            ])
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
