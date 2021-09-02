# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os

import llnl.util.tty as tty

from spack import *


class Umpire(CMakePackage, CudaPackage, ROCmPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = 'https://github.com/LLNL/Umpire'
    git      = 'https://github.com/LLNL/Umpire.git'

    maintainers = ['davidbeckingsale']

    version('develop', branch='develop', submodules=True)
    version('main', branch='main', submodules=True)
    version('6.0.0', tag='v6.0.0', submodules=True)
    version('5.0.1', tag='v5.0.1', submodules=True)
    version('5.0.0', tag='v5.0.0', submodules=True)
    version('4.1.2', tag='v4.1.2', submodules=True)
    version('4.1.1', tag='v4.1.1', submodules=True)
    version('4.1.0', tag='v4.1.0', submodules=True)
    version('4.0.1', tag='v4.0.1', submodules=True)
    version('4.0.0', tag='v4.0.0', submodules=True)
    version('3.0.0', tag='v3.0.0', submodules=True)
    version('2.1.0', tag='v2.1.0', submodules=True)
    version('2.0.0', tag='v2.0.0', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)
    version('1.0.1', tag='v1.0.1', submodules=True)
    version('1.0.0', tag='v1.0.0', submodules=True)
    version('0.3.5', tag='v0.3.5', submodules=True)
    version('0.3.4', tag='v0.3.4', submodules=True)
    version('0.3.3', tag='v0.3.3', submodules=True)
    version('0.3.2', tag='v0.3.2', submodules=True)
    version('0.3.1', tag='v0.3.1', submodules=True)
    version('0.3.0', tag='v0.3.0', submodules=True)
    version('0.2.4', tag='v0.2.4', submodules=True)
    version('0.2.3', tag='v0.2.3', submodules=True)
    version('0.2.2', tag='v0.2.2', submodules=True)
    version('0.2.1', tag='v0.2.1', submodules=True)
    version('0.2.0', tag='v0.2.0', submodules=True)
    version('0.1.4', tag='v0.1.4', submodules=True)
    version('0.1.3', tag='v0.1.3', submodules=True)

    patch('camp_target_umpire_3.0.0.patch', when='@3.0.0')
    patch('cmake_version_check.patch', when='@4.1')
    patch('missing_header_for_numeric_limits.patch', when='@4.1:5.0.1')

    variant('fortran', default=False, description='Build C/Fortran API')
    variant('c', default=True, description='Build C API')
    variant('numa', default=False, description='Enable NUMA support')
    variant('shared', default=True, description='Enable Shared libs')
    variant('openmp', default=False, description='Build with OpenMP support')
    variant('deviceconst', default=False,
            description='Enables support for constant device memory')
    variant('examples', default=True, description='Build Umpire Examples')
    variant('tests', default='none', values=('none', 'basic', 'benchmarks'),
            multi=False, description='Tests to run')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', when='+cuda', type='build')

    depends_on('blt@0.4.1:', type='build', when='@6.0.0:')
    depends_on('blt@0.4.0:', type='build', when='@4.1.3:5.0.1')
    depends_on('blt@0.3.6:', type='build', when='@:4.1.2')

    depends_on('camp', when='@5.0.0:')
    depends_on('camp@0.2.2', when='@6.0.0:')
    depends_on('camp@0.1.0', when='@5.0.0:5.0.1')

    with when('@5.0.0:'):
        with when('+cuda'):
            depends_on('camp+cuda')
            for sm_ in CudaPackage.cuda_arch_values:
                depends_on('camp+cuda cuda_arch={0}'.format(sm_),
                           when='cuda_arch={0}'.format(sm_))

        with when('+rocm'):
            depends_on('camp+rocm')
            for arch_ in ROCmPackage.amdgpu_targets:
                depends_on('camp+rocm amdgpu_target={0}'.format(arch_),
                           when='amdgpu_target={0}'.format(arch_))

    conflicts('+numa', when='@:0.3.2')
    conflicts('~c', when='+fortran', msg='Fortran API requires C API')

    # device allocator exports device code, which requires static libs
    # currently only available for cuda.
    conflicts('+shared', when='+cuda')

    def cmake_args(self):
        spec = self.spec

        options = []
        options.append("-DBLT_SOURCE_DIR={0}".format(spec['blt'].prefix))
        if spec.satisfies('@5.0.0:'):
            options.append("-Dcamp_DIR={0}".format(spec['camp'].prefix))

        if '+cuda' in spec:
            options.extend([
                '-DENABLE_CUDA=On',
                '-DCUDA_TOOLKIT_ROOT_DIR=%s' % (spec['cuda'].prefix)])

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                options.append('-DCUDA_ARCH=sm_{0}'.format(cuda_arch[0]))
                options.append('-DCMAKE_CUDA_ARCHITECTURES={0}'.format(cuda_arch[0]))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                options.append('-DCMAKE_CUDA_FLAGS:STRING={0}'.format(flag))

            if '+deviceconst' in spec:
                options.append('-DENABLE_DEVICE_CONST=On')
        else:
            options.append('-DENABLE_CUDA=Off')

        if '+rocm' in spec:
            options.extend([
                '-DENABLE_HIP=ON',
                '-DHIP_ROOT_DIR={0}'.format(spec['hip'].prefix)
            ])
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                options.append(
                    '-DHIP_HIPCC_FLAGS=--amdgpu-target={0}'.format(arch_str)
                )
        else:
            options.append('-DENABLE_HIP=OFF')

        options.append('-DENABLE_C={0}'.format(
            'On' if '+c' in spec else 'Off'))

        options.append('-DENABLE_FORTRAN={0}'.format(
            'On' if '+fortran' in spec else 'Off'))

        options.append('-DENABLE_NUMA={0}'.format(
            'On' if '+numa' in spec else 'Off'))

        options.append('-DENABLE_OPENMP={0}'.format(
            'On' if '+openmp' in spec else 'Off'))

        options.append('-DBUILD_SHARED_LIBS={0}'.format(
            'On' if '+shared' in spec else 'Off'))

        options.append('-DENABLE_BENCHMARKS={0}'.format(
            'On' if 'tests=benchmarks' in spec else 'Off'))

        options.append('-DENABLE_EXAMPLES={0}'.format(
            'On' if '+examples' in spec else 'Off'))

        options.append('-DENABLE_TESTS={0}'.format(
            'Off' if 'tests=none' in spec else 'On'))

        return options

    def test(self):
        """Perform stand-alone checks on the installed package."""
        if self.spec.satisfies('@:1') or \
                not os.path.isdir(self.prefix.bin):
            tty.info('Skipping: checks not installed in bin for v{0}'.
                     format(self.version))
            return

        # Run a subset of examples PROVIDED installed
        # tutorials with readily checkable outputs.
        checks = {
            'malloc': ['99 should be 99'],
            'recipe_dynamic_pool_heuristic': ['in the pool', 'releas'],
            'recipe_no_introspection': ['has allocated', 'used'],
            'strategy_example': ['Available allocators', 'HOST'],
            'tut_copy': ['Copied source data'],
            'tut_introspection':
                ['Allocator used is HOST', 'size of the allocation'],
            'tut_memset': ['Set data from HOST'],
            'tut_move': ['Moved source data', 'HOST'],
            'tut_reallocate': ['Reallocated data'],
            'vector_allocator': [''],
        }

        for exe in checks:
            expected = checks[exe]
            reason = 'test: checking output from {0}'.format(exe)
            self.run_test(exe, [], expected, 0, installed=False,
                          purpose=reason, skip_missing=True,
                          work_dir=self.prefix.bin)
