# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT/"
    url      = "https://github.com/ROCmSoftwarePlatform/rocfft/archive/rocm-3.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']

    version('3.5.0', sha256='629f02cfecb7de5ad2517b6a8aac6ed4de60d3a9c620413c4d9db46081ac2c88')

    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012'
    )

    variant('build_type', default='Release', values=("Release", "Debug"), description='CMake build type')
    variant('amdgpu_target', default='gfx701', multi=True, values=amdgpu_targets)

    depends_on('cmake@3:', type='build')
    depends_on('rocm-cmake@3.5.0', type='build', when='@3.5.0')
    depends_on('rocm-device-libs@3.5.0', type='build', when='@3.5.0')

    depends_on('hip@3.5.0', type=('build', 'link'), when='@3.5.0')
    depends_on('comgr@3.5.0', type='build', when='@3.5.0')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        archs = ",".join(self.spec.variants['amdgpu_target'].value)

        args = [
            '-DCMAKE_CXX_FLAGS=--amdgpu-target={0}'.format(archs),
        ]
        return args
