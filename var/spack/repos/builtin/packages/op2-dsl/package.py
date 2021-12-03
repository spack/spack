# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Op2Dsl(MakefilePackage):
    """OP2 is a high-level embedded domain specific language for writing
    unstructured mesh algorithms with automatic parallelisation on multi-core
    and many-core architectures."""

    homepage = "https://op-dsl.github.io/"
    git      = "https://github.com/OP-DSL/OP2-Common.git"

    maintainers = ['gihanmudalige', 'reguly', 'bozbez']
    version('master', branch='master')

    build_directory = 'op2'

    variant('mpi', default=True, description='Enable MPI support')
    variant('cuda', default=False, description='Enable CUDA support')

    variant('parmetis', default=True,
            description='Enable ParMETIS partitioning support for MPI')

    variant('scotch', default=True,
            description='Enable PT-Scotch partitioning support for MPI')

    depends_on('cuda', when='+cuda')

    with when('+mpi'):
        depends_on('mpi')

        depends_on('parmetis', when='+parmetis')
        depends_on('scotch', when='+scotch')

        depends_on('hdf5+fortran+mpi')

    with when('~mpi'):
        depends_on('hdf5+fortran~mpi')

        conflicts('+parmetis', msg='ParMETIS partitioning support requires MPI')
        conflicts('+scotch', msg='PT-Scotch partitioning support requires MPI')

    depends_on('gmake', type='build')

    def edit(self, spec, prefix):
        compiler_map = {
            '%gcc': 'gnu',
            '%cce': 'cray',
            '%intel': 'intel',
            '%nvhpc': 'nvhpc',
            '%xl': 'xl',
        }

        for compiler in compiler_map.keys():
            if compiler in self.spec:
                env['OP2_COMPILER'] = compiler_map[compiler]
                break

    def install(self, spec, prefix):
        install_tree('op2/lib', prefix.lib)
        install_tree('op2/include', prefix.include)
        install_tree('op2/mod', prefix.mod)
