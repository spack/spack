# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.package_defs import *


class Comgr(CMakePackage):
    """This provides various Lightning Compiler related services. It currently
       contains one library, the Code Object Manager (Comgr)"""

    homepage = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport"
    git      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport.git"
    url      = "https://github.com/RadeonOpenCompute/ROCm-CompilerSupport/archive/rocm-4.5.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('master', branch='amd-stg-open')

    version('5.1.0', sha256='1cdcfe5acb768ef50fb0026d4ee7ba01e615251ad3c27bb2593cdcf8c070a894')
    version('5.0.2', sha256='20d733f70d8edb573d8c92707f663d7d46dcaff08026cd6addbb83266679f92a')
    version('5.0.0', sha256='da1bbc694bd930a504406eb0a0018c2e317d8b2c136fb2cab8de426870efe9a8')
    version('4.5.2', sha256='e45f387fb6635fc1713714d09364204cd28fea97655b313c857beb1f8524e593')
    version('4.5.0', sha256='03c5880e0922fcff31306f7da2eb9d3a3709d9b5b75b3524dcfae85f4b181678')
    version('4.3.1', sha256='f1d99550383ed7b3a01d304eedc3d86a8e45b271aa5a80b1dd099c22fda3f745')
    version('4.3.0', sha256='f77b505abb474078374701dfc49e651ad3eeec5349ce6edda54549943a3775ee')
    version('4.2.0', sha256='40a1ea50d2aea0cf75c4d17cdd6a7fe44ae999bf0147d24a756ca4675ce24e36')
    version('4.1.0', sha256='ffb625978555c63582aa46857672431793261166aa31761eff4fe5c2cab661ae', deprecated=True)
    version('4.0.0', sha256='f389601fb70b2d9a60d0e2798919af9ddf7b8376a2e460141507fe50073dfb31', deprecated=True)
    version('3.10.0', sha256='b44ee5805a6236213d758fa4b612bb859d8f774b9b4bdc3a2699bb009dd631bc', deprecated=True)
    version('3.9.0', sha256='6600e144d72dadb6d893a3388b42af103b9443755ce556f4e9e205ccd8ec0c83', deprecated=True)
    version('3.8.0', sha256='62a35480dfabaa98883d91ed0f7c490daa9bbd424af37e07e5d85a6e8030b146', deprecated=True)
    version('3.7.0', sha256='73e56ec3c63dade24ad351e9340e2f8e127694028c1fb7cec5035376bf098432', deprecated=True)
    version('3.5.0', sha256='25c963b46a82d76d55b2302e0e18aac8175362656a465549999ad13d07b689b9', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    # Disable the hip compile tests.  Spack should not be using
    # /opt/rocm, and this breaks the build when /opt/rocm exists.
    patch('hip-tests.patch', when='@:4.2.0')

    depends_on('cmake@3.2.0:',  type='build', when='@:3.8')
    depends_on('cmake@3.13.4:', type='build', when='@3.9.0:')

    depends_on('zlib', type='link')
    depends_on('z3', type='link')
    depends_on('ncurses', type='link')

    depends_on('rocm-cmake@3.5.0:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0', 'master']:
        # llvm libs are linked statically, so this *could* be a build dep
        depends_on('llvm-amdgpu@' + ver, when='@' + ver)

        # aomp may not build rocm-device-libs as part of llvm-amdgpu, so make
        # that a conditional dependency
        depends_on('rocm-device-libs@' + ver, when='@{0} ^llvm-amdgpu ~rocm-device-libs'.format(ver))

    root_cmakelists_dir = join_path('lib', 'comgr')
