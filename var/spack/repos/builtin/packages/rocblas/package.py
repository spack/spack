# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack.util.package import *


class Rocblas(CMakePackage):
    """Radeon Open Compute BLAS library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocBLAS/"
    git      = "https://github.com/ROCmSoftwarePlatform/rocBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocBLAS/archive/rocm-5.0.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('5.1.0', sha256='efa0c424b5ada697314aa8a78c19c93ade15f1612c4bfc8c53d71d1c9719aaa3')
    version('5.0.2', sha256='358a0902fc279bfc80205659a90e96269cb7d83a80386b121e4e3dfe221fec23')
    version('5.0.0', sha256='4b01fba937ada774f09c7ccb5e9fdc66e1a5d46c130be833e3706e6b5841b1da')
    version('4.5.2', sha256='15d725e38f91d1ff7772c4204b97c1515af58fa7b8ec2a2014b99b6d337909c4')
    version('4.5.0', sha256='22d15a1389a10f1324f5e0ceac1a6ec0758a2801a18419a55e37e2bc63793eaf')
    version('4.3.1', sha256='ad3c09573cb2bcfdb12bfb5a05e85f9c95073993fd610981df24dda792727b4b')
    version('4.3.0', sha256='b15a66c861b3394cb83c56b64530b2c7e57b2b4c50f55d0e66bb3d1483b50ec4')
    version('4.2.0', sha256='547f6d5d38a41786839f01c5bfa46ffe9937b389193a8891f251e276a1a47fb0')
    version('4.1.0', sha256='8be20c722bab169bc4badd79a9eab9a1aa338e0e5ff58ad85ba6bf09e8ac60f4', deprecated=True)
    version('4.0.0', sha256='78e37a7597b581d90a29e4b956fa65d0f8d1c8fb51667906b5fe2a223338d401', deprecated=True)
    version('3.10.0', sha256='9bfd0cf99662192b1ac105ab387531cfa9338ae615db80ed690c6a14d987e0e8', deprecated=True)
    version('3.9.0', sha256='3ecd2d9fd2be0e1697a191d143a2d447b53a91ae01afb50231d591136ad5e2fe', deprecated=True)
    version('3.8.0', sha256='568a9da0360349b1b134d74cc67cbb69b43c06eeca7c33b50072cd26cd3d8900', deprecated=True)
    version('3.7.0', sha256='9425db5f8e8b6f7fb172d09e2a360025b63a4e54414607709efc5acb28819642', deprecated=True)
    version('3.5.0', sha256='8560fabef7f13e8d67da997de2295399f6ec595edfd77e452978c140d5f936f0', deprecated=True)

    amdgpu_targets = ('gfx906', 'gfx908', 'gfx803', 'gfx900',
                      'gfx906:xnack-', 'gfx908:xnack-', 'gfx90a:xnack+',
                      'gfx90a:xnack-', 'gfx1010', 'gfx1011',
                      'gfx1012', 'gfx1030')

    variant('amdgpu_target', values=auto_or_any_combination_of(*amdgpu_targets))
    variant('tensile', default=True, description='Use Tensile as a backend')
    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    # gfx906, gfx908,gfx803,gfx900 are valid for @:4.0.0
    # gfx803,gfx900,gfx:xnack-,gfx908:xnack- are valid gpus for @4.1.0:4.2.0
    # gfx803 till gfx1030  are valid gpus for @4.3.0:
    conflicts('amdgpu_target=gfx906', when='@4.0.1:')
    conflicts('amdgpu_target=gfx908', when='@4.0.1:')
    conflicts('amdgpu_target=gfx906:xnack-', when='@:4.0.0')
    conflicts('amdgpu_target=gfx908:xnack-', when='@:4.0.0')
    conflicts('amdgpu_target=gfx90a:xnack+', when='@:4.2.1')
    conflicts('amdgpu_target=gfx90a:xnack-', when='@:4.2.1')
    conflicts('amdgpu_target=gfx1010', when='@:4.2.1')
    conflicts('amdgpu_target=gfx1011', when='@:4.2.1')
    conflicts('amdgpu_target=gfx1012', when='@:4.2.1')
    conflicts('amdgpu_target=gfx1030', when='@:4.2.1')

    depends_on('cmake@3.16.8:', type='build', when='@4.2.0:')
    depends_on('cmake@3.8:', type='build', when='@3.9.0:')
    depends_on('cmake@3.5:', type='build')

    depends_on('googletest@1.10.0:', type='test')
    depends_on('netlib-lapack@3.7.1:', type='test')

    def check(self):
        if '@4.2.0:' in self.spec:
            exe = join_path(self.build_directory, 'clients', 'staging', 'rocblas-test')
            self.run_test(exe, options=['--gtest_filter=*quick*-*known_bug*'])

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0', '5.0.2',
                '5.1.0']:
        depends_on('hip@' + ver,                         when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,                 when='@' + ver)
        depends_on('rocminfo@' + ver,     type='build',  when='@' + ver)
        depends_on('rocm-cmake@%s:' % ver, type='build', when='@' + ver)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0']:
        depends_on('rocm-smi@' + ver, type='build', when='@' + ver)

    for ver in ['4.0.0', '4.1.0', '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2',
                '5.0.0', '5.0.2', '5.1.0']:
        depends_on('rocm-smi-lib@' + ver, type='build', when='@' + ver)

    # This is the default library format since 3.7.0
    depends_on('msgpack-c@3:', when='@3.7:')

    depends_on('python@3.6:', type='build')
    depends_on('py-virtualenv', type='build')
    depends_on('perl-file-which', type='build')
    depends_on('py-pyyaml', type='build')
    depends_on('py-wheel', type='build')
    depends_on('py-msgpack', type='build')
    depends_on('py-pip', type='build')

    for t_version, t_commit in [
        ('@3.5.0',  'f842a1a4427624eff6cbddb2405c36dec9a210cd'),
        ('@3.7.0',  'af71ea890a893e647bf2cf4571a90297d65689ca'),
        ('@3.8.0',  '9123205f9b5f95c96ff955695e942d2c3b321cbf'),
        ('@3.9.0',  'b68edc65aaeed08c71b2b8622f69f83498b57d7a'),
        ('@3.10.0', 'ab44bf46b609b5a40053f310bef2ab7511f726ae'),
        ('@4.0.0',  'ab44bf46b609b5a40053f310bef2ab7511f726ae'),
        ('@4.1.0',  'd175277084d3253401583aa030aba121e8875bfd'),
        ('@4.2.0',  '3438af228dc812768b20a068b0285122f327fa5b'),
        ('@4.3.0',  '9cbabb07f81e932b9c98bf5ae48fbd7fcef615cf'),
        ('@4.3.1',  '9cbabb07f81e932b9c98bf5ae48fbd7fcef615cf'),
        ('@4.5.0',  '0f6a6d1557868d6d563cb1edf167c32c2e34fda0'),
        ('@4.5.2',  '0f6a6d1557868d6d563cb1edf167c32c2e34fda0'),
        ('@5.0.0',  '75b9aefe5981d85d1df32ddcebf32dab52bfdabd'),
        ('@5.0.2',  '75b9aefe5981d85d1df32ddcebf32dab52bfdabd'),
        ('@5.1.0',  'ea38f8661281a37cd81c96cc07868e3f07d2c4da')
    ]:
        resource(name='Tensile',
                 git='https://github.com/ROCmSoftwarePlatform/Tensile.git',
                 commit=t_commit,
                 when='{} +tensile'.format(t_version))

    # Status: https://github.com/ROCmSoftwarePlatform/Tensile/commit/a488f7dadba34f84b9658ba92ce9ec5a0615a087
    # Not yet landed in 3.7.0, nor 3.8.0.
    patch('0001-Fix-compilation-error-with-StringRef-to-basic-string.patch', when='@:3.8')
    patch('0002-Fix-rocblas-clients-blas.patch', when='@4.2.0:4.3.1')
    patch('0003-Fix-rocblas-gentest.patch', when='@4.2.0:')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = [
            self.define('BUILD_CLIENTS_TESTS',
                        self.run_tests and '@4.2.0:' in self.spec),
            self.define('BUILD_CLIENTS_BENCHMARKS', 'OFF'),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('RUN_HEADER_TESTING', 'OFF'),
            self.define_from_variant('BUILD_WITH_TENSILE', 'tensile'),
        ]
        if self.run_tests:
            args.append(self.define('LINK_BLIS', 'OFF'))

        arch_define_name = 'AMDGPU_TARGETS'
        if '+tensile' in self.spec:
            tensile_path = join_path(self.stage.source_path, 'Tensile')
            args += [
                self.define('Tensile_TEST_LOCAL_PATH', tensile_path),
                self.define('Tensile_COMPILER', 'hipcc'),
                self.define('Tensile_LOGIC', 'asm_full'),
                self.define('Tensile_CODE_OBJECT_VERSION', 'V3'),
                self.define('BUILD_WITH_TENSILE_HOST', '@3.7.0:' in self.spec)
            ]
            if self.spec.satisfies('@3.7.0:'):
                args.append(self.define('Tensile_LIBRARY_FORMAT', 'msgpack'))
            if self.spec.satisfies('@:4.2.0'):
                arch_define_name = 'Tensile_ARCHITECTURE'

        # See https://github.com/ROCmSoftwarePlatform/rocBLAS/commit/c1895ba4bb3f4f5947f3818ebd155cf71a27b634
        if 'auto' not in self.spec.variants['amdgpu_target']:
            args.append(self.define_from_variant(arch_define_name, 'amdgpu_target'))

        # See https://github.com/ROCmSoftwarePlatform/rocBLAS/issues/1196
        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
