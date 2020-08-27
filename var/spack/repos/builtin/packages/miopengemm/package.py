# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Miopengemm(CMakePackage):
    """An OpenCL general matrix multiplication (GEMM) API
    and kernel generator"""

    homepage = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM"
    url      = "https://github.com/ROCmSoftwarePlatform/MIOpenGEMM/archive/1.1.6.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('1.1.6', sha256='9ab04903794c6a59432928eaec92c687d51e2b4fd29630cf227cbc49d56dc69b')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@1.1.6')
    depends_on('rocm-opencl@3.5:', type='build', when='@1.1.6')
