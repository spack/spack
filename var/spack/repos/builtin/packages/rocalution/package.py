# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocalution(CMakePackage):
    """rocALUTION is a sparse linear algebra library with focus on
       exploring fine-grained parallelism on top of AMD's Radeon Open
       eCosystem Platform ROCm runtime and toolchains, targeting modern
       CPU and GPU platforms. Based on C++ and HIP, it provides a portable,
        generic and flexible design that allows seamless integration with
       other scientific software packages."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocALUTION"
    git      = "https://github.com/ROCmSoftwarePlatform/rocALUTION.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocALUTION/archive/rocm-4.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('master', branch='develop')
    version('4.5.2', sha256='8be38922320cd9d4fc465a30f0322843849f62c0c7dad2bdbe52290a1b69d2a0')
    version('4.5.0', sha256='191629fef002fd1a0793a6b4fe5a6b8c43ac49d3cd173ba64a91359f54659e5b')
    version('4.3.1', sha256='d3a7b9290f99bdc7382d1d5259c3f5e0e66a43aef4d05b7c2cd78b0e4a5c59bc')
    version('4.3.0', sha256='f064b96f9f04cf22b89f95f72147fcfef28e2c56ecd764008c060f869c74c144')
    version('4.2.0', sha256='0424adf522ded41de5b77666e04464a25c73c92e34025762f30837f90a797445')
    version('4.1.0', sha256='3f61be18a02dff0c152a0ad7eb4779c43dd744b0ba172aa6a4267fc596d582e4', deprecated=True)
    version('4.0.0', sha256='80a224a5c19dea290e6edc0e170c3dff2e726c2b3105d599ec6858cc66f076a9', deprecated=True)
    version('3.10.0', sha256='c24cb9d1a8a1a3118040b8b16dec7c06268bcf157424d3378256cc9eb93f1b58', deprecated=True)
    version('3.9.0', sha256='1ce36801fe1d44f743b46b43345c0cd90d76b73911b2ec97be763f93a35396fb', deprecated=True)
    version('3.8.0', sha256='39e64a29e75c4276163a93596436064c6338770ca72ce7f43711ed8285ed2de5', deprecated=True)
    version('3.7.0', sha256='4d6b20aaaac3bafb7ec084d684417bf578349203b0f9f54168f669e3ec5699f8', deprecated=True)
    version('3.5.0', sha256='be2f78c10c100d7fd9df5dd2403a44700219c2cbabaacf2ea50a6e2241df7bfe', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.5:', type='build')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', 'master']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocblas@' + ver, when='@' + ver)
        depends_on('rocprim@' + ver, when='@' + ver)
        depends_on('rocsparse@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    for ver in ['3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0',
                '4.3.0', '4.3.1', '4.5.0', '4.5.2', 'master']:
        depends_on('rocrand@' + ver, when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def patch(self):
        if '@3.9.0:' in self.spec:
            kwargs = {'ignore_absent': False, 'backup': False, 'string': False}

            with working_dir('src/base/hip'):
                match = '^#include <rocrand/rocrand.hpp>'
                substitute = "#include <rocrand.hpp>"
                files = ['hip_rand_normal.hpp', 'hip_rand_uniform.hpp']
                filter_file(match, substitute, *files, **kwargs)

    def cmake_args(self):
        args = [
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake),
            self.define('SUPPORT_HIP', 'ON'),
            self.define('SUPPORT_MPI', 'OFF'),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF')
        ]

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
