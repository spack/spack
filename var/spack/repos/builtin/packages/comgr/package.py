# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
       contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    url      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9')

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0']:
        depends_on('llvm-amdgpu@' + ver, type='build', when='@' + ver)
        depends_on('rocm-device-libs@' + ver, type='build', when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    depends_on('zlib', type='link')
    depends_on('z3', type='link')
    depends_on('ncurses', type='link')

    root_cmakelists_dir = 'lib/comgr'
