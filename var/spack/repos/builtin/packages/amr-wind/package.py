# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack import *


class AmrWind(CMakePackage, CudaPackage, ROCmPackage):
    """AMR-Wind is a massively parallel, block-structured adaptive-mesh,
    incompressible flow sover for wind turbine and wind farm simulations. """

    homepage = "https://github.com/Exawind/amr-wind"
    git      = "https://github.com/Exawind/amr-wind.git"

    maintainers = ['jrood-nrel']

    tags = ['ecp', 'ecp-apps']

    version('main', branch='main', submodules=True)

    variant('hypre', default=True,
            description='Enable Hypre integration')
    variant('masa', default=False,
            description='Enable MASA integration')
    variant('mpi', default=True,
            description='Enable MPI support')
    variant('netcdf', default=True,
            description='Enable NetCDF support')
    variant('openfast', default=False,
            description='Enable OpenFAST integration')
    variant('openmp', default=False,
            description='Enable OpenMP for CPU builds')
    variant('shared', default=True,
            description='Build shared libraries')
    variant('tests', default=True,
            description='Activate regression tests')

    depends_on('hypre~int64+shared@2.20.0:', when='+hypre')
    depends_on('hypre+mpi', when='+mpi')
    for arch in CudaPackage.cuda_arch_values:
        depends_on('hypre+unified-memory+cuda cuda_arch=%s' % arch,
                   when='+cuda+hypre cuda_arch=%s' % arch)
    for arch in ROCmPackage.amdgpu_targets:
        depends_on('hypre+rocm amdgpu_target=%s' % arch,
                   when='+rocm+hypre amdgpu_target=%s' % arch)
    depends_on('masa', when='+masa')
    depends_on('mpi', when='+mpi')
    depends_on('netcdf-c', when='+netcdf')
    depends_on('openfast+cxx', when='+openfast')
    depends_on('py-matplotlib', when='+masa')
    depends_on('py-pandas', when='+masa')

    conflicts('+openmp', when='+cuda')
    conflicts('+shared', when='+cuda')

    def setup_build_environment(self, env):
        # Avoid compile errors with Intel interprocedural optimization
        if '%intel' in self.spec:
            env.append_flags('CXXFLAGS', '-no-ipo')

    def cmake_args(self):
        define = CMakePackage.define

        vs = ["mpi", "cuda", "openmp", "netcdf", "hypre", "masa",
              "openfast", "rocm", "tests"]
        args = [
            self.define_from_variant("AMR_WIND_ENABLE_%s" % v.upper(), v)
            for v in vs
        ]

        args += [
            define('AMR_WIND_ENABLE_ALL_WARNINGS', True),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
        ]

        if '+mpi' in self.spec:
            args.append(define('MPI_HOME', self.spec['mpi'].prefix))

        if '+cuda' in self.spec:
            amrex_arch = ['{0:.1f}'.format(float(i) / 10.0)
                          for i in self.spec.variants['cuda_arch'].value]
            if amrex_arch:
                args.append(define('AMReX_CUDA_ARCH', amrex_arch))

        if '+rocm' in self.spec:
            args.append(define('CMAKE_CXX_COMPILER', self.spec['hip'].hipcc))
            targets = self.spec.variants['amdgpu_target'].value
            args.append('-DAMReX_AMD_ARCH=' + ';'.join(str(x) for x in targets))

        return args
