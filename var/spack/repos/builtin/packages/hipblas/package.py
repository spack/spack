# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipblas(CMakePackage):
    """hipBLAS is a BLAS marshalling library, with multiple
       supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    git      = "https://github.com/ROCmSoftwarePlatform/hipBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('4.3.1', sha256='7b1f774774de5fa3d2b777e3a262328559d56165c32aa91b002505694362e7b2')
    version('4.3.0', sha256='0631e21c588794ea1c8413ef8ff293606bcf7a52c0c3ff88da824f103395a76a')
    version('4.2.0', sha256='c7ce7f69c7596b5a54e666fb1373ef41d1f896dd29260a691e2eadfa863e2b1a')
    version('4.1.0', sha256='876efe80a4109ad53d290d2921b3fb425b4cb857b32920819f10dcd4deee4ef8')
    version('4.0.0', sha256='6cc03af891b36cce8266d32ba8dfcf7fdfcc18afa7a6cc058fbe28bcf8528d94')
    version('3.10.0', sha256='45cb5e3b37f0845bd9e0d09912df4fa0ce88dd508ec9448241ae6600d3c4b1e8')
    version('3.9.0', sha256='82ddd57fd905a5d4060665349ec017ff757a7c121cb9310574be3c3630b3545f')
    version('3.8.0', sha256='33cb82e8b2658ae2096f39e41492ba8b6852ac37c26a730612b8642d9d29abe3')
    version('3.7.0', sha256='9840a493ab4838c86696ceb33ce07c34b5f59f62db4f88cb3af62b69d84f8729')
    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1')

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocsolver@' + ver, when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def cmake_args(self):
        args = [
            # Make sure find_package(HIP) finds the module.
            self.define('CMAKE_MODULE_PATH', self.spec['hip'].prefix.cmake),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('BUILD_CLIENTS_TESTS', 'OFF')
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
