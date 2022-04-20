# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack import *


class Rocsparse(CMakePackage):
    """rocSPARSE exposes a common interface that provides
    Basic Linear Algebra Subroutines for sparse computation
    implemented on top of AMD's Radeon Open eCosystem Platform ROCm runtime
    and toolchains. rocSPARSE is created using the HIP programming
    language and optimized for AMD's latest discrete GPUs."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSPARSE"
    git      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSPARSE/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    amdgpu_targets = ('gfx803', 'gfx900:xnack-', 'gfx906:xnack-', 'gfx908:xnack-',
                      'gfx90a:xnack-', 'gfx90a:xnack+',
                      'gfx1030')

    variant('amdgpu_target', values=auto_or_any_combination_of(*amdgpu_targets))
    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    version('5.0.2', sha256='c9d9e1b7859e1c5aa5050f5dfdf86245cbd7c1296c0ce60d9ca5f3e22a9b748b')
    version('5.0.0', sha256='6d352bf27dbed08e5115a58815aa76c59eb2008ec9dcc921aadf2efe20115d2a')
    version('4.5.2', sha256='e37af2cd097e239a55a278df534183b5591ef4d985fe1a268a229bd11ada6599')
    version('4.5.0', sha256='b120e9e17e7e141caee4c8c4288c9d1902bad0cec2ea76458d3ba11343376938')
    version('4.3.1', sha256='fa5ea64f71e1cfbebe41618cc183f501b387824a6dc58486ab1214d7af5cbef2')
    version('4.3.0', sha256='1a8109bdc8863b3acfe991449360c9361cae7cabdbe753c553bc57872cd0ad5e')
    version('4.2.0', sha256='8a86ed49d278e234c82e406a1430dc28f50d416f8f1065cf5bdf25cc5721129c')
    version('4.1.0', sha256='7514968ed2342dc274acce8b269c128a6aa96cce769a37fd3880b5269c2ed17f', deprecated=True)
    version('4.0.0', sha256='2b41bc6623d204ad7f351a902810f34cd32b762d1bf59081dbb00f83e689a794', deprecated=True)
    version('3.10.0', sha256='8325828c5d7818dfb45e03b5f1572a573cc21964d596aaaa33b7469817b03abd', deprecated=True)
    version('3.9.0', sha256='7b8f952d0c7f8ac2f3bb60879ab420fabbfafb0885a3d8464d5b4c191e97dec6', deprecated=True)
    version('3.8.0', sha256='a5d085fffe05a7ac7f5658075d9782b9b02d0c5c3e2c1807dad266c3a61141fd', deprecated=True)
    version('3.7.0', sha256='db561ae5e8ee117f7c539a9ef6ee49c13b82ba9f702b22c76e741cca245386a9', deprecated=True)
    version('3.5.0', sha256='9ca6bae7da78abbb47143c3d77ff4a8cd7d63979875fc7ebc46b400769fd9cb5', deprecated=True)

    depends_on('cmake@3.5:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2']:
        depends_on('hip@' + ver, when='@' + ver)
        for tgt in itertools.chain(['auto'], amdgpu_targets):
            depends_on('rocprim@{0} amdgpu_target={1}'.format(ver, tgt),
                       when='@{0} amdgpu_target={1}'.format(ver, tgt))
        depends_on('rocm-cmake@%s:' % ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('BUILD_CLIENTS_TESTS', 'OFF'),
            self.define('BUILD_CLIENTS_BENCHMARKS', 'OFF')
        ]

        if 'auto' not in self.spec.variants['amdgpu_target']:
            args.append(self.define_from_variant('AMDGPU_TARGETS', 'amdgpu_target'))

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
