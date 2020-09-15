# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocsolver(CMakePackage):
    """rocSOLVER is a work-in-progress implementation of a
       subset of LAPACK functionality on the ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSOLVER"
    git      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.7.0', sha256='8c1c630595952806e658c539fd0f3056bd45bafc22b57f0dd10141abefbe4595')
    version('3.5.0', sha256='d655e8c762fb9e123b9fd7200b4258512ceef69973de4d0588c815bc666cb358')

    depends_on('cmake@3:', type='build')
    depends_on('numactl', when='^hip@3.7.0')
    depends_on('hsa-rocr-dev@3.7.0', type='build', when='@3.7.0')

    for ver in ['3.5.0', '3.7.0']:
        depends_on('hip@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('comgr@' + ver, type='build', when='@' + ver)
        depends_on('rocblas@' + ver, type='link', when='@' + ver)

    def cmake_args(self):
        args = [
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF',
            '-DBUILD_CLIENTS_BENCHMARKS=OFF'
        ]
        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
