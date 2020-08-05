# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocminfo(CMakePackage):
    """Radeon Open Compute (ROCm) Runtime rocminfo tool"""

    homepage = "https://github.com/RadeonOpenCompute/rocminfo"
    url      = "https://github.com/RadeonOpenCompute/rocminfo/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='1d113f06b7c9b60d0e92b2c12c0c704a565696867496fe7038e5dddd510567b7')

    depends_on('cmake@3:', type='build')
    depends_on('hsakmt-roct@3.5.0', type='build', when='@3.5.0')
    depends_on('hsa-rocr-dev@3.5.0', type='build', when='@3.5.0')

    def cmake_args(self):
        args = ['-DROCM_DIR={0}'.format(self.spec['hsa-rocr-dev'].prefix)]
        return args
