# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import re

from spack.package import *


class Hipblas(CMakePackage):
    """hipBLAS is a BLAS marshalling library, with multiple
       supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    git      = "https://github.com/ROCmSoftwarePlatform/hipBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']
    libraries = ['libhipblas.so']

    version('5.1.0', sha256='22faba3828e50a4c4e22f569a7d6441c797a11db1d472619c01d3515a3275e92')
    version('5.0.2', sha256='201772bfc422ecb2c50e898dccd7d3d376cf34a2b795360e34bf71326aa37646')
    version('5.0.0', sha256='63cffe748ed4a86fc80f408cb9e8a9c6c55c22a2b65c0eb9a76360b97bbb9d41')
    version('4.5.2', sha256='82dd82a41bbadbb2a91a2a44a5d8e0d2e4f36d3078286ed4db3549b1fb6d6978')
    version('4.5.0', sha256='187777ed49cc7c496c897e8ba80532d458c9afbc51a960e45f96923ad896c18e')
    version('4.3.1', sha256='7b1f774774de5fa3d2b777e3a262328559d56165c32aa91b002505694362e7b2')
    version('4.3.0', sha256='0631e21c588794ea1c8413ef8ff293606bcf7a52c0c3ff88da824f103395a76a')
    version('4.2.0', sha256='c7ce7f69c7596b5a54e666fb1373ef41d1f896dd29260a691e2eadfa863e2b1a')
    version('4.1.0', sha256='876efe80a4109ad53d290d2921b3fb425b4cb857b32920819f10dcd4deee4ef8', deprecated=True)
    version('4.0.0', sha256='6cc03af891b36cce8266d32ba8dfcf7fdfcc18afa7a6cc058fbe28bcf8528d94', deprecated=True)
    version('3.10.0', sha256='45cb5e3b37f0845bd9e0d09912df4fa0ce88dd508ec9448241ae6600d3c4b1e8', deprecated=True)
    version('3.9.0', sha256='82ddd57fd905a5d4060665349ec017ff757a7c121cb9310574be3c3630b3545f', deprecated=True)
    version('3.8.0', sha256='33cb82e8b2658ae2096f39e41492ba8b6852ac37c26a730612b8642d9d29abe3', deprecated=True)
    version('3.7.0', sha256='9840a493ab4838c86696ceb33ce07c34b5f59f62db4f88cb3af62b69d84f8729', deprecated=True)
    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.5:', type='build')

    depends_on('googletest@1.10.0:', type='test')
    depends_on('netlib-lapack@3.7.1:', type='test')
    depends_on('boost@1.64.0:1.76.0 cxxstd=14', type='test')

    patch('link-clients-blas.patch', when='@4.3.0:4.3.2')
    patch('link-clients-blas-4.5.0.patch', when='@4.5.0:4.5.2')
    patch('hipblas-link-clients-blas-5.0.0.patch', when='@5.0.0:5.0.2')

    def check(self):
        exe = join_path(self.build_directory, 'clients', 'staging', 'hipblas-test')
        self.run_test(exe)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2', '5.1.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocsolver@' + ver, when='@' + ver)
        depends_on('rocblas@' + ver, when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@%s:' % ver, type='build', when='@' + ver)

    @classmethod
    def determine_version(cls, lib):
        match = re.search(r'lib\S*\.so\.\d+\.\d+\.(\d)(\d\d)(\d\d)',
                          lib)
        if match:
            ver = '{0}.{1}.{2}'.format(int(match.group(1)),
                                       int(match.group(2)),
                                       int(match.group(3)))
        else:
            ver = None
        return ver

    def cmake_args(self):
        args = [
            # Make sure find_package(HIP) finds the module.
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('BUILD_CLIENTS_TESTS', self.run_tests)
        ]

        # hipblas actually prefers CUDA over AMD GPUs when you have it
        # installed...
        if self.spec.satisfies('@:3.9.0'):
            args.append(self.define('TRY_CUDA', 'OFF'))
        else:
            args.append(self.define('USE_CUDA', 'OFF'))

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
