# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipblas(CMakePackage):
    """hipBLAS is a BLAS marshalling library, with multiple
       supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipBLAS"
    git      = "https://github.com/ROCmSoftwarePlatform/hipBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipBLAS/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    for ver in ['3.5.0', '3.7.0']:
        depends_on('hip@' + ver, when='@' + ver)
        depends_on('rocsolver@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)

    version('3.7.0', sha256='9840a493ab4838c86696ceb33ce07c34b5f59f62db4f88cb3af62b69d84f8729')
    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1')

    def cmake_args(self):
        args = [
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF'
        ]
        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
