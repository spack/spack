# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class Rocblas(CMakePackage):
    """Radeon Open Compute BLAS library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocBLAS/"
    git      = "https://github.com/ROCmSoftwarePlatform/rocBLAS.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocBLAS/archive/rocm-4.3.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']
    version('4.3.1', sha256='ad3c09573cb2bcfdb12bfb5a05e85f9c95073993fd610981df24dda792727b4b')
    version('4.3.0', sha256='b15a66c861b3394cb83c56b64530b2c7e57b2b4c50f55d0e66bb3d1483b50ec4')
    version('4.2.0', sha256='547f6d5d38a41786839f01c5bfa46ffe9937b389193a8891f251e276a1a47fb0')
    version('4.1.0', sha256='8be20c722bab169bc4badd79a9eab9a1aa338e0e5ff58ad85ba6bf09e8ac60f4')
    version('4.0.0', sha256='78e37a7597b581d90a29e4b956fa65d0f8d1c8fb51667906b5fe2a223338d401')
    version('3.10.0', sha256='9bfd0cf99662192b1ac105ab387531cfa9338ae615db80ed690c6a14d987e0e8')
    version('3.9.0', sha256='3ecd2d9fd2be0e1697a191d143a2d447b53a91ae01afb50231d591136ad5e2fe')
    version('3.8.0', sha256='568a9da0360349b1b134d74cc67cbb69b43c06eeca7c33b50072cd26cd3d8900')
    version('3.7.0', sha256='9425db5f8e8b6f7fb172d09e2a360025b63a4e54414607709efc5acb28819642')
    version('3.5.0', sha256='8560fabef7f13e8d67da997de2295399f6ec595edfd77e452978c140d5f936f0')

    tensile_architecture = ('all', 'gfx803', 'gfx900', 'gfx906', 'gfx908')

    variant('tensile_architecture', default='all', values=tensile_architecture, multi=False)

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1']:
        depends_on('hip@' + ver,                       when='@' + ver)
        depends_on('llvm-amdgpu@' + ver,               when='@' + ver)
        depends_on('rocm-cmake@' + ver,  type='build', when='@' + ver)
        depends_on('rocminfo@' + ver,    type='build', when='@' + ver)

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0']:
        depends_on('rocm-smi@' + ver, type='build', when='@' + ver)

    for ver in ['4.0.0', '4.1.0', '4.2.0', '4.3.0', '4.3.1']:
        depends_on('rocm-smi-lib@' + ver, type='build', when='@' + ver)

    # This is the default library format since 3.7.0
    depends_on('msgpack-c@3:', when='@3.7:')

    depends_on('python', type='build')
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
        ('@4.3.1',  '9cbabb07f81e932b9c98bf5ae48fbd7fcef615cf')
    ]:
        resource(name='Tensile',
                 git='https://github.com/ROCmSoftwarePlatform/Tensile.git',
                 commit=t_commit,
                 when=t_version)

    # Status: https://github.com/ROCmSoftwarePlatform/Tensile/commit/a488f7dadba34f84b9658ba92ce9ec5a0615a087
    # Not yet landed in 3.7.0, nor 3.8.0.
    patch('0001-Fix-compilation-error-with-StringRef-to-basic-string.patch', when='@:3.8')

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        arch = self.spec.variants['tensile_architecture'].value
        if self.spec.satisfies('@4.1.0:'):
            if arch == 'gfx906' or arch == 'gfx908':
                arch = arch + ':xnack-'

        tensile = join_path(self.stage.source_path, 'Tensile')

        args = [
            self.define('BUILD_CLIENTS_TESTS', 'OFF'),
            self.define('BUILD_CLIENTS_BENCHMARKS', 'OFF'),
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('RUN_HEADER_TESTING', 'OFF'),
            self.define('BUILD_WITH_TENSILE', 'ON'),
            self.define('Tensile_TEST_LOCAL_PATH', tensile),
            self.define('Tensile_COMPILER', 'hipcc'),
            self.define('Tensile_LOGIC', 'asm_full'),
            self.define('Tensile_CODE_OBJECT_VERSION', 'V3'),
            self.define(
                'BUILD_WITH_TENSILE_HOST',
                'ON' if '@3.7.0:' in self.spec else 'OFF'
            )
        ]

        if '@3.7.0:' in self.spec:
            args.append(self.define('Tensile_LIBRARY_FORMAT', 'msgpack'))

        # See https://github.com/ROCmSoftwarePlatform/rocBLAS/commit/c1895ba4bb3f4f5947f3818ebd155cf71a27b634
        if self.spec.satisfies('@:4.2.0'):
            args.append(self.define('Tensile_ARCHITECTURE', arch))
        else:
            args.append(self.define('AMDGPU_TARGETS', arch))

        # See https://github.com/ROCmSoftwarePlatform/rocBLAS/issues/1196
        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
