# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RocmClangOcl(CMakePackage):
    """ OpenCL compilation with clang compiler """

    homepage = "https://github.com/RadeonOpenCompute/clang-ocl"
    url      = "https://github.com/RadeonOpenCompute/clang-ocl/archive/rocm-3.8.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.8.0', sha256='a829aa2efb6e3bc00d8a08a96404f937f3c8adf3b4922b5ac35050d6e08b912d')
    version('3.7.0', sha256='9c00c7e7dd3ac8326ae6772a43866b44ae049d5960ea6993d14a2370db74d326')
    version('3.5.0', sha256='38c95fbd0ac3d11d9bd224ad333b68b9620dde502b8a8a9f3d96ba642901e8bb')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0']:
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
