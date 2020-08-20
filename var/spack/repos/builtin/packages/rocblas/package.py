# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocblas(CMakePackage):
    """Radeon Open Compute BLAS library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocBLAS/"
    url      = "https://github.com/ROCmSoftwarePlatform/rocBLAS/archive/rocm-3.5.0.tar.gz"

    maintainers = ['haampie']

    version('3.5.0', sha256='8560fabef7f13e8d67da997de2295399f6ec595edfd77e452978c140d5f936f0')

    amdgpu_targets = ('all', 'gfx803', 'gfx900', 'gfx906', 'gfx908')

    variant('amdgpu_target', default='all', multi=True, values=amdgpu_targets)

    depends_on('cmake@3:', type='build')
    depends_on('rocm-cmake@3.5.0', type='build', when='@3.5.0')
    depends_on('rocm-device-libs@3.5.0', type='build', when='@3.5.0')

    depends_on('hip@3.5.0', when='@3.5.0')
    depends_on('comgr@3.5.0', type='build', when='@3.5.0')

    depends_on('python', type='build')
    depends_on('py-virtualenv', type='build')
    depends_on('perl-file-which', type='build')
    depends_on('py-pyyaml', type='build')
    depends_on('py-wheel', type='build')

    # Tensile uses LLVM
    depends_on('llvm-amdgpu')

    resource(name='Tensile',
             git='https://github.com/ROCmSoftwarePlatform/Tensile.git',
             commit='f842a1a4427624eff6cbddb2405c36dec9a210cd',
             when='@3.5.0')

    patch('0001-Fix-compilation-error-with-StringRef-to-basic-string.patch')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        archs = ",".join(self.spec.variants['amdgpu_target'].value)

        tensile = join_path(self.stage.source_path, 'Tensile')

        args = [
            '-Damd_comgr_DIR={0}'.format(self.spec['comgr'].prefix),
            '-DBUILD_CLIENTS_TESTS=OFF',
            '-DBUILD_CLIENTS_BENCHMARKS=OFF',
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DRUN_HEADER_TESTING=OFF',
            '-DBUILD_WITH_TENSILE=ON',
            '-DBUILD_WITH_TENSILE_HOST=OFF',
            '-DTensile_TEST_LOCAL_PATH={0}'.format(tensile),
            '-DTensile_COMPILER=hipcc',
            '-DTensile_ARCHITECTURE={0}'.format(archs),
            '-DTensile_LOGIC=asm_full',
            '-DTensile_CODE_OBJECT_VERSION=V3'
        ]

        return args
