# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class Hipfort(CMakePackage):
    """ Radeon Open Compute Parallel Primitives Library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/hipfort"
    git      = "https://github.com/ROCmSoftwarePlatform/hipfort.git"
    url      = "https://github.com/ROCmSoftwarePlatform/hipfort/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('5.0.2', sha256='fcee6e62482ab15f365681dbc12bd9ae26b0fab2f2848a3c14de8ec63004a7aa')
    version('5.0.0', sha256='af0f332fec082a03ca0403618ab20d31baadf3103e3371db9edc39dc9474ef4c')
    version('4.5.2', sha256='14599d027b57189c6734b04ace7792d2ae5c409cf7983c0970b086fb4e634dd8')
    version('4.5.0', sha256='48626dfb15bb5dcb044c9e1d4dc4b0654a2cd0abfc69485aa285dc20d7f40d51')
    version('4.3.1', sha256='279a35edbc0c22fa930a4355e663a86adf4d0316c5b1b6b9ccc6ee5c19c8c2e4')
    version('4.3.0', sha256='fd0ffdafdc17ac42c7dae3f89991651f15affdef9b2354da05c7493d09d8974e')
    version('4.2.0', sha256='b411cb32bf87927eba4c5573b412c56d75d15165e2f1c8ac5ac18e624ed3a4b4')
    version('4.1.0', sha256='2d335ae068d0cbb480575de7d3ea4868362af32cb195f911ee1aeced499f3974', deprecated=True)
    version('4.0.0', sha256='a497645c33e0eff39abd5344756de63424733cde2837b7376c924b44ed5ae9c9', deprecated=True)
    version('3.10.0', sha256='44173522d9eb2a18ec1cea2d9b00b237fe70501f0849bd6be3decbb73389487a', deprecated=True)
    version('3.9.0', sha256='a3c4e125a9b56820446a65bd76b8caa196fddb0e0723eb513f0bcde9abd6a0c0', deprecated=True)
    version('3.8.0', sha256='0132e9949f758dd8b8a462d133b3316101440cd503aa6c53bea9e34e61bbb3cc', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.0.2:', type='build')

    depends_on('rocm-cmake@3.8.0:', type='build')

    for ver in ['3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0',
                '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2']:
        depends_on('hip@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = []

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
