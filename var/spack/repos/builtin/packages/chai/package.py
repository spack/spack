# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import socket

from spack import *


class Chai(CachedCMakePackage, CudaPackage, ROCmPackage):
    """
    Copy-hiding array interface for data migration between memory spaces
    """

    homepage = "https://github.com/LLNL/CHAI"
    git      = "https://github.com/LLNL/CHAI.git"
    tags     = ['ecp', 'e4s', 'radiuss']

    maintainers = ['davidbeckingsale']

    version('develop', branch='develop', submodules=True)
    version('main', branch='main', submodules=True)
    version('2022.03.0', tag='v2022.03.0', submodules=True)
    version('2.4.0', tag='v2.4.0', submodules=True)
    version('2.3.0', tag='v2.3.0', submodules=True)
    version('2.2.2', tag='v2.2.2', submodules=True)
    version('2.2.1', tag='v2.2.1', submodules=True)
    version('2.2.0', tag='v2.2.0', submodules=True)
    version('2.1.1', tag='v2.1.1', submodules=True)
    version('2.1.0', tag='v2.1.0', submodules=True)
    version('2.0.0', tag='v2.0.0', submodules=True)
    version('1.2.0', tag='v1.2.0', submodules=True)
    version('1.1.0', tag='v1.1.0', submodules=True)
    version('1.0', tag='v1.0', submodules=True)

    variant('enable_pick', default=False, description='Enable pick method')
    variant('shared', default=True, description='Build Shared Libs')
    variant('raja', default=False, description='Build plugin for RAJA')
    variant('benchmarks', default=False, description='Build benchmarks.')
    variant('examples', default=True, description='Build examples.')
    variant('openmp', default=False, description='Build using OpenMP')
    # TODO: figure out gtest dependency and then set this default True
    # and remove the +tests conflict below.
    variant('tests', default=False, description='Build tests')

    depends_on('cmake@3.8:', type='build')
    depends_on('cmake@3.9:', type='build', when="+cuda")
    depends_on('cmake@3.14:', when='@2022.03.0:')

    depends_on('blt@0.5.0:', type='build', when='@2022.03.0:')
    depends_on('blt@0.4.1:', type='build', when='@2.4.0:')
    depends_on('blt@0.4.0:', type='build', when='@2.3.0')
    depends_on('blt@0.3.6:', type='build', when='@:2.2.2')

    depends_on('umpire')
    depends_on('umpire@2022.03.0', when='@2022.03.0')
    depends_on('umpire@6.0.0', when="@2.4.0")
    depends_on('umpire@4.1.2', when="@2.2.0:2.3.0")
    depends_on('umpire@main', when='@main')

    with when('+cuda'):
        depends_on('umpire+cuda')
        for sm_ in CudaPackage.cuda_arch_values:
            depends_on('umpire+cuda cuda_arch={0}'.format(sm_),
                       when='cuda_arch={0}'.format(sm_))

    with when('+rocm'):
        depends_on('umpire+rocm')
        for arch in ROCmPackage.amdgpu_targets:
            depends_on('umpire+rocm amdgpu_target={0}'.format(arch),
                       when='amdgpu_target={0}'.format(arch))

    with when('+raja'):
        depends_on('raja~openmp', when='~openmp')
        depends_on('raja+openmp', when='+openmp')
        depends_on('raja@0.14.0', when="@2.4.0")
        depends_on('raja@0.13.0', when="@2.3.0")
        depends_on('raja@0.12.0', when="@2.2.0:2.2.2")
        depends_on('raja@2022.03.0', when='@2022.03.0')
        depends_on('raja@main', when='@main')

        with when('+cuda'):
            depends_on('raja+cuda')
            for sm_ in CudaPackage.cuda_arch_values:
                depends_on('raja+cuda cuda_arch={0}'.format(sm_),
                           when='cuda_arch={0}'.format(sm_))
        with when('+rocm'):
            depends_on('raja+rocm')
            for arch in ROCmPackage.amdgpu_targets:
                depends_on('raja+rocm amdgpu_target={0}'.format(arch),
                           when='amdgpu_target={0}'.format(arch))

    conflicts('+benchmarks', when='~tests')

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

    def initconfig_hardware_entries(self):
        spec = self.spec
        entries = super(Chai, self).initconfig_hardware_entries()

        entries.append(cmake_cache_option("ENABLE_OPENMP", '+openmp' in spec))

        if '+cuda' in spec:
            entries.append(cmake_cache_option("ENABLE_CUDA", True))
            entries.append(cmake_cache_option("CMAKE_CUDA_SEPARABLE_COMPILATION", True))
            entries.append(cmake_cache_option("CUDA_SEPARABLE_COMPILATION", True))

            if not spec.satisfies('cuda_arch=none'):
                cuda_arch = spec.variants['cuda_arch'].value
                entries.append(cmake_cache_string(
                    "CUDA_ARCH", 'sm_{0}'.format(cuda_arch[0])))
                entries.append(cmake_cache_string(
                    "CMAKE_CUDA_ARCHITECTURES", '{0}'.format(cuda_arch[0])))
                flag = '-arch sm_{0}'.format(cuda_arch[0])
                entries.append(cmake_cache_string(
                    "CMAKE_CUDA_FLAGS", '{0}'.format(flag)))
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

        entries.append(cmake_cache_path("BLT_SOURCE_DIR", spec['blt'].prefix))
        if '+raja' in spec:
            entries.append(cmake_cache_option("CHAI_ENABLE_RAJA_PLUGIN", True))
            entries.append(cmake_cache_path("RAJA_DIR", spec['raja'].prefix))
        entries.append(cmake_cache_option('CHAI_ENABLE_PICK', '+enable_pick' in spec))
        entries.append(cmake_cache_path(
            "umpire_DIR", spec['umpire'].prefix.share.umpire.cmake))
        entries.append(cmake_cache_option("ENABLE_TESTS", '+tests' in spec))
        entries.append(cmake_cache_option("ENABLE_BENCHMARKS", '+benchmarks' in spec))
        entries.append(cmake_cache_option("CHAI_ENABLE_EXAMPLES", '+examples' in spec))
        entries.append(cmake_cache_option("BUILD_SHARED_LIBS", '+shared' in spec))

        return entries

    def cmake_args(self):
        options = []
        return options
