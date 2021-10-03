# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# This is a partial copy of Spack Gromacs package
# - modified URL and versions
# - removed Plumed patches
# - calling original patch and cmake-related procedures to not duplicate them
# - simplified variants/dependencies because this fork starts at Gromacs 2021

import os

from spack.pkg.builtin.gromacs import Gromacs as BuiltinGromacs


class GromacsChainCoordinate(CMakePackage):
    """
    A modification of GROMACS that implements the "chain coordinate", a reaction
    coordinate for pore formation in membranes and stalk formation between membranes.
    """

    homepage = 'https://gitlab.com/cbjh/gromacs-chain-coordinate/-/blob/main/README.md'
    url = 'https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.1/gromacs-chain-coordinate-release-2021.chaincoord-0.1.tar.bz2'
    git = 'https://gitlab.com/cbjh/gromacs-chain-coordinate.git'
    maintainers = ['w8jcik']

    version('main', branch='main')
    version('2021.2-0.1', sha256="879fdd04662370a76408b72c9fbc4aff60a6387b459322ac2700d27359d0dd87",
            url="https://gitlab.com/cbjh/gromacs-chain-coordinate/-/archive/release-2021.chaincoord-0.1/gromacs-chain-coordinate-release-2021.chaincoord-0.1.tar.bz2",
            preferred=True)

    variant('mpi', default=True,
            description='Activate MPI support (disable for Thread-MPI support)')
    variant('shared', default=True,
            description='Enables the build of shared libraries')
    variant(
        'double', default=False,
        description='Produces a double precision version of the executables')
    variant('cuda', default=False, description='Enable CUDA support')
    variant('opencl', default=False, description='Enable OpenCL support')
    variant('sycl', default=False, description='Enable SYCL support')
    variant('nosuffix', default=False, description='Disable default suffixes')
    variant('build_type', default='RelWithDebInfo',
            description='The build type to build',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel',
                    'Reference', 'RelWithAssert', 'Profile'))
    variant('openmp', default=True,
            description='Enables OpenMP at configure time')
    variant('hwloc', default=True,
            description='Use the hwloc portable hardware locality library')
    variant('lapack', default=False,
            description='Enables an external LAPACK library')
    variant('blas', default=False,
            description='Enables an external BLAS library')
    variant('cycle_subcounters', default=False,
            description='Enables cycle subcounters')

    depends_on('mpi', when='+mpi')
    depends_on('fftw-api@3')
    depends_on('cmake@3.16.0:3', type='build')
    depends_on('cuda', when='+cuda')
    depends_on('sycl', when='+sycl')
    depends_on('lapack', when='+lapack')
    depends_on('blas', when='+blas')
    depends_on('hwloc', when='+hwloc')

    filter_compiler_wrappers(
        '*.cmake',
        relative_root=os.path.join('share', 'cmake', 'gromacs_mpi'))
    filter_compiler_wrappers(
        '*.cmake',
        relative_root=os.path.join('share', 'cmake', 'gromacs'))

    def patch(self):
        BuiltinGromacs.patch(self)

    def cmake_args(self):
        return super(GromacsChainCoordinate, self).cmake_args()

    def check(self):
        """The default 'test' targets does not compile the test programs"""
        with working_dir(self.build_directory):
            if self.generator == 'Unix Makefiles':
                self._if_make_target_execute('check')
            elif self.generator == 'Ninja':
                self._if_ninja_target_execute('check')
