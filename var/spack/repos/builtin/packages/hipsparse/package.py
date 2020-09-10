# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Hipsparse(CMakePackage):
    """hipSPARSE is a SPARSE marshalling library, with
       multiple supported backends"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipSPARSE"
    git      = "https://github.com/ROCmSoftwarePlatform/hipSPARSE.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipSPARSE/archive/rocm-3.5.0.tar.gz"

    maintainers = ['haampie']

    version('3.5.0', sha256='fa16b2a307a5d9716066c2876febcbc1cef855bf0c96d235d2d8f2206a0fb69d')

    depends_on('hip')
    depends_on('rocsparse')
    depends_on('rocm-device-libs', type='build')
    depends_on('hsa-rocr-dev')
    depends_on('comgr', type='build')
    depends_on('git', type='build')

    patch('e79985dccde22d826aceb3badfc643a3227979d2.patch')
    patch('530047af4a0f437dafc02f76b3a17e3b1536c7ec.patch')

    def cmake_args(self):
        args = [
            '-DCMAKE_CXX_STANDARD=14',
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DBUILD_CLIENTS_TESTS=OFF',
        ]
        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
