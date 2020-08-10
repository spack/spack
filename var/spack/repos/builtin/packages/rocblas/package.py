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

    amdgpu_targets = (
        'gfx701', 'gfx801', 'gfx802', 'gfx803',
        'gfx900', 'gfx906', 'gfx908', 'gfx1010',
        'gfx1011', 'gfx1012'
    )

    variant('amdgpu_target', default='gfx701', multi=True, values=amdgpu_targets)

    variant('tensile', default=True, description='Use the Tensile client for GEMM')

    depends_on('cmake@3:', type='build')
    depends_on('rocm-cmake@3.5.0', type='build', when='@3.5.0')
    depends_on('rocm-device-libs@3.5.0', type='build', when='@3.5.0')

    depends_on('hip@3.5.0', type=('build', 'link'), when='@3.5.0')
    depends_on('comgr@3.5.0', type='build', when='@3.5.0')

    depends_on('python', type='build', when='+tensile')
    depends_on('py-virtualenv', type='build', when='+tensile')
    depends_on('perl-file-which', type='build', when='+tensile')
    depends_on('py-pyyaml', type='build', when='+tensile')
    depends_on('py-wheel', type='build', when='+tensile')

    resource(name='tensile',
            url='https://github.com/ROCmSoftwarePlatform/Tensile/archive/rocm-3.5.0.tar.gz',
            sha256='71eb3eed6625b08a4cedb539dd9b596e3d4cc82a1a8063d37d94c0765b6f8257',
            when='@3.5.0 +tensile')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        archs = ",".join(self.spec.variants['amdgpu_target'].value)

        args = [
            # '-DCMAKE_CXX_FLAGS=--amdgpu-target={0}'.format(archs),
            '-Damd_comgr_DIR={0}'.format(self.spec['comgr'].prefix),
            '-DBUILD_CLIENTS_TESTS=OFF',
            '-DBUILD_CLIENTS_BENCHMARKS=OFF',
            '-DBUILD_CLIENTS_SAMPLES=OFF',
            '-DRUN_HEADER_TESTING=OFF'
        ]

        if '+tensile' in self.spec:
            tensile = join_path(
                self.stage.source_path,
                'Tensile-rocm-{0}'.format(self.version)
            )

            args.extend([
                '-DBUILD_WITH_TENSILE=ON',
                '-DTensile_TEST_LOCAL_PATH={0}'.format(tensile),
                '-DTensile_COMPILER=hipcc',
                '-DTensile_ARCHITECTURE={0}'.format(archs),
                '-DTensile_LOGIC=asm_full',
            ])

        else:
            args.extend([
                '-DBUILD_WITH_TENSILE=OFF',
                '-DAMDGPU_TARGETS={0}'.format(archs),
            ]) 

        return args
