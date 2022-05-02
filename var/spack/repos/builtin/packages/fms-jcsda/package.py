# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class FmsJcsda(CMakePackage):
    """GFDL's Flexible Modeling System (FMS) is a software environment
    that supports the efficient development, construction, execution,
    and scientific interpretation of atmospheric, oceanic, and climate
    system models.
    This version has been adapated by JCSDA and is only meant to be
    used temporarily, until the JCSDA changes have found their way
    back into the official repository."""

    #homepage = "https://github.com/jcsda/fms"
    #git = "https://github.com/jcsda/fms.git"
    homepage = "https://github.com/climbfuji/fms"
    git = "https://github.com/climbfuji/fms.git"

    maintainers = ['climbfuji']

    version('release-stable', branch='feature/no-openmp-option_default_on', no_cache=True, preferred=True)
    version('dev-jcsda',      branch='dev/jcsda',      no_cache=True)

    variant('64bit',                 default=True,  description='64 bit?')
    variant('gfs_phys',              default=True,  description='Use GFS Physics?')
    variant('openmp',                default=True,  description='Use OpenMP?')
    variant('enable_quad_precision', default=True,  description='Enable quad precision?')
    variant('pic',                   default=True,  description='Generate position-independent code (PIC), useful '
                                                               'for building static libraries')
    depends_on('mpi')
    depends_on('netcdf-c')
    depends_on('netcdf-fortran')
    depends_on('ecbuild', type=('build'), when='@release-stable')
    depends_on('jedi-cmake', type=('build'), when='@release-stable')

    def cmake_args(self):
        args = [
            self.define_from_variant('64BIT'),
            self.define_from_variant('GFS_PHYS'),
            self.define_from_variant('OPENMP'),
            self.define_from_variant('ENABLE_QUAD_PRECISION')
        ]

        args.append(self.define('CMAKE_C_COMPILER', self.spec['mpi'].mpicc))
        args.append(self.define('CMAKE_CXX_COMPILER', self.spec['mpi'].mpicxx))
        args.append(self.define('CMAKE_Fortran_COMPILER', self.spec['mpi'].mpifc))

        cflags = []
        fflags = []

        if self.compiler.name in ['gcc', 'clang', 'apple-clang']:
            gfortran_major_version = int(spack.compiler.get_compiler_version_output(self.compiler.fc, '-dumpversion').split('.')[0])
            if gfortran_major_version>=10:
                fflags.append('-fallow-argument-mismatch')

        if '+pic' in self.spec:
            cflags.append(self.compiler.cc_pic_flag)
            fflags.append(self.compiler.fc_pic_flag)

        if cflags:
            args.append(self.define('CMAKE_C_FLAGS', ' '.join(cflags)))
        if fflags:
            args.append(self.define('CMAKE_Fortran_FLAGS', ' '.join(fflags)))

        return args
