# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *

class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    url      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3.5.2', type='build')
    depends_on('rocm-cmake@3.5:', type='build', when='@3.5:')
    depends_on('llvm-amdgpu@3.5:', type='build', when='@3.5:')
    depends_on('rocm-device-libs@3.5:', type='build', when='@3.5:')

    root_cmakelists_dir = 'lib/comgr'

    def cmake_args(self):
        spec=self.spec
        args = [
                '-DCMAKE_VERBOSE_MAKEFILE=1',
                '-DCMAKE_INSTALL_RPATH_USE_LINK_PATH="FALSE"'
               ]

        return args
