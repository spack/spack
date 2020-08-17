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

    maintainers = ['haampie']

    depends_on('hip')
    depends_on('rocsolver')
    depends_on('rocblas')
    depends_on('rocm-device-libs', type='build')
    depends_on('comgr', type='build')

    version('3.5.0', sha256='d451da80beb048767da71a090afceed2e111d01b3e95a7044deada5054d6e7b1')

    def cmake_args(self):
        args = [
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF'
        ]
        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
