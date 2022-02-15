# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os
import socket

import llnl.util.tty as tty

from spack import *


class Umpire(CachedCMakePackage, CudaPackage, ROCmPackage):
    """An application-focused API for memory management on NUMA & GPU
    architectures"""

    homepage = 'https://github.com/LLNL/Umpire'
    git      = 'https://github.com/LLNL/Umpire.git'
    tags     = ['radiuss', 'e4s']

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

    # export targets when building pre-6.0.0 release with BLT 0.4.0+
    patch('https://github.com/LLNL/Umpire/commit/5773ce9af88952c8d23f9bcdcb2e503ceda40763.patch',
          sha256='f5c691752e4833a936bce224bbe0fe884d3afa84c5e5a4a481f59a12840159c9',
          when='@:5.0.1 ^blt@0.4:')

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
    depends_on('cmake@:3.20', when='+rocm', type='build')

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

    # https://github.com/LLNL/Umpire/issues/653
    # This range looks weird, but it ensures the concretizer looks at it as a
    # range, not as a concrete version, so that it also matches 10.3.* versions.
    conflicts('%gcc@10.3.0:10.3', when='+cuda')

    def _get_sys_type(self, spec):
        sys_type = spec.architecture
        if "SYS_TYPE" in env:
            sys_type = env["SYS_TYPE"]
        return sys_type

    @property
    def cache_name(self):
        hostname = socket.gethostname()
        if "SYS_TYPE" in env:
            hostname = hostname.rstrip('1234567890')
        return "{0}-{1}-{2}@{3}.cmake".format(
            hostname,
            self._get_sys_type(self.spec),
            self.spec.compiler.name,
            self.spec.compiler.version
        )

    def initconfig_compiler_entries(self):
        spec = self.spec
        entries = super(Umpire, self).initconfig_compiler_entries()

        if '+fortran' in spec and self.compiler.fc is not None:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", True))
        else:
            entries.append(cmake_cache_option("ENABLE_FORTRAN", False))

        entries.append(cmake_cache_option("ENABLE_C", '+c' in spec))

        return entries

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Umpire, self).initconfig_hardware_entries()

        if '+cuda' in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                entries.append(cmake_cache_string(
                    "CUDA_ARCH", 'sm_{0}'.format(cuda_arch[0])))
                entries.append(cmake_cache_string(
                    "CMAKE_CUDA_ARCHITECTURES", '{0}'.format(cuda_arch[0])))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                entries.append(cmake_cache_string(
                    "CMAKE_CUDA_FLAGS", '{0}'.format(flag)))

            entries.append(cmake_cache_option(
                "ENABLE_DEVICE_CONST", spec.satisfies('+deviceconst')))
        else:
            entries.append(cmake_cache_option("ENABLE_CUDA", False))

        if '+rocm' in spec:
            entries.append(cmake_cache_option("ENABLE_HIP", True))
            entries.append(cmake_cache_path(
                "HIP_ROOT_DIR", '{0}'.format(spec['hip'].prefix)))
            archs = self.spec.variants['amdgpu_target'].value
            if archs != 'none':
                arch_str = ",".join(archs)
                entries.append(cmake_cache_string(
                    "HIP_HIPCC_FLAGS", '--amdgpu-target={0}'.format(arch_str)))
        else:
            entries.append(cmake_cache_option("ENABLE_HIP", False))

        return entries

    def initconfig_package_entries(self):
        spec = self.spec
        entries = []

        # TPL locations
        entries.append("#------------------{0}".format("-" * 60))
        entries.append("# TPLs")
        entries.append("#------------------{0}\n".format("-" * 60))

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec['blt'].prefix))
        if spec.satisfies('@5.0.0:'):
            entries.append(cmake_cache_path("camp_DIR", spec['camp'].prefix))
        entries.append(cmake_cache_option("ENABLE_NUMA", '+numa' in spec))
        entries.append(cmake_cache_option("ENABLE_OPENMP", '+openmp' in spec))
        entries.append(cmake_cache_option(
            "ENABLE_BENCHMARKS", 'tests=benchmarks' in spec))
        entries.append(cmake_cache_option("ENABLE_EXAMPLES", '+examples' in spec))
        entries.append(cmake_cache_option("ENABLE_DOCS", False))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", '+shared' in spec))
        entries.append(cmake_cache_option("ENABLE_TESTS", 'tests=none' not in spec))

        return entries

    def cmake_args(self):
        options = []
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
