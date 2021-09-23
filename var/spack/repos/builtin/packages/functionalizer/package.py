##############################################################################
# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class Functionalizer(CMakePackage):
    """Apply several steps of filtering on touches
    """
    homepage = "https://bbpgitlab.epfl.ch/hpc/archive/functionalizer"
    git      = "git@bbpgitlab.epfl.ch:hpc/archive/functionalizer.git"

    version('develop', branch='master', submodules=True)
    version('3.12.2', tag='v3.12.2', submodules=True)
    version('3.12.1', tag='v3.12.1', submodules=True)
    version('3.12.0', tag='v3.12.0', submodules=True)
    version('3.11.0',
            commit='50c83265c100cec66a27eea9311b58a9b652cb5f',
            submodules=True)
    version('gap-junctions',
            commit='6095a851119d8125a81f2858c7a0de2ff6f012d6',
            submodules=True)

    depends_on('boost@1.50:')
    depends_on('cmake', type='build')
    depends_on('cmake@:3.0.0', type='build', when='@gap-junctions')
    depends_on('hpctools~openmp')
    depends_on('hpctools~openmp@:3.1', when='@gap-junctions')
    depends_on('hdf5@1.8:')
    depends_on('libxml2')
    depends_on('pkg-config', type='build')
    depends_on('mpi')
    depends_on('zlib')

    def patch(self):
        """Prevent `-isystem /usr/include` from appearing, since this confuses gcc.
        """
        if self.spec.satisfies('@gap-junctions'):
            return
        filter_file(r'(include_directories\()SYSTEM ',
                    r'\1',
                    'functionalizer/CMakeLists.txt')

    def cmake_args(self):
        args = [
            '-DCMAKE_C_COMPILER={0}'.format(self.spec['mpi'].mpicc),
            '-DCMAKE_CXX_COMPILER={0}'.format(self.spec['mpi'].mpicxx)
        ]
        return args
