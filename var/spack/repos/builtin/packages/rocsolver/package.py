# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import itertools

from spack import *


class Rocsolver(CMakePackage):
    """rocSOLVER is a work-in-progress implementation of a
       subset of LAPACK functionality on the ROCm platform."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocSOLVER"
    git      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocSOLVER/archive/rocm-5.0.2.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    amdgpu_targets = (
        'gfx803', 'gfx900', 'gfx906:xnack-', 'gfx908:xnack-',
        'gfx90a:xnack-', 'gfx90a:xnack+', 'gfx1010', 'gfx1011', 'gfx1012', 'gfx1030'
    )
    variant('amdgpu_target', values=auto_or_any_combination_of(*amdgpu_targets))
    variant('optimal', default=True,
            description='This option improves performance at the cost of increased binary \
            size and compile time by adding specialized kernels \
            for small matrix sizes')

    version('5.0.2', sha256='298e0903f1ba8074055ab072690f967062d6e06a9371574de23e4e38d2997688')
    version('5.0.0', sha256='d444ad5348eb8a2c04646ceae6923467a0e775441f2c73150892e228e585b2e1')
    version('4.5.2', sha256='4639322bd1e77fedfdeb9032633bde6211a0b1cc16a612db7754f873f18a492f')
    version('4.5.0', sha256='0295862da941f31f4d43b19195b79331bd17f5968032f75c89d2791a6f8c1e8c')
    version('4.3.1', sha256='c6e7468d7041718ce6e1c7f50ec80a552439ac9cfed2dc3f753ae417dda5724f')
    version('4.3.0', sha256='63cc88dd285c0fe01ec2394321ec3b4e1e59bb98ce05b06e4b4d8fadcf1ff028')
    version('4.2.0', sha256='e9ef72d7c29e7c36bf02be63a64ca23b444e1ca71751749f7d66647873d9fdea')
    version('4.1.0', sha256='da5cc800dabf7367b02b73c93780b2967f112bb45232e4b06e5fd07b4d5b8d88', deprecated=True)
    version('4.0.0', sha256='be9a52644c276813f76d78f2c11eddaf8c2d7f9dd04f4570f23d328ad30d5880', deprecated=True)
    version('3.10.0', sha256='bc72483656b6b23a1e321913a580ca460da3bc5976404647536a01857f178dd2', deprecated=True)
    version('3.9.0', sha256='85fd77fe5acf5af518d11e90e2c03ee0c5abd61071cea86ef5df09f944879648', deprecated=True)
    version('3.8.0', sha256='72aa74284944d8b454088e8c8d74cf05464a4e2e46d33a57017ddd009113025e', deprecated=True)
    version('3.7.0', sha256='8c1c630595952806e658c539fd0f3056bd45bafc22b57f0dd10141abefbe4595', deprecated=True)
    version('3.5.0', sha256='d655e8c762fb9e123b9fd7200b4258512ceef69973de4d0588c815bc666cb358', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    depends_on('cmake@3.8:', type='build', when='@4.1.0:')
    depends_on('cmake@3.5:', type='build')
    depends_on('fmt@7:8.0.1', type='build', when='@4.5.0:')

    depends_on('googletest@1.10.0:', type='test')
    depends_on('netlib-lapack@3.7.1:', type='test')

    patch('link-clients-blas.patch', when='@4.3.0:4.3.2')

    def check(self):
        exe = join_path(self.build_directory, 'clients', 'staging', 'rocsolver-test')
        self.run_test(exe, options=['--gtest_filter=checkin*'])

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', '5.0.0',
                '5.0.2']:
        depends_on('hip@' + ver, when='@' + ver)
        for tgt in itertools.chain(['auto'], amdgpu_targets):
            depends_on('rocblas@{0} amdgpu_target={1}'.format(ver, tgt),
                       when='@{0} amdgpu_target={1}'.format(ver, tgt))
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def cmake_args(self):
        args = [
            self.define('BUILD_CLIENTS_SAMPLES', 'OFF'),
            self.define('BUILD_CLIENTS_TESTS', self.run_tests),
            self.define('BUILD_CLIENTS_BENCHMARKS', 'OFF')
        ]
        if self.spec.satisfies('@4.1.0'):
            incl = self.spec['rocblas'].prefix
            args.append(self.define(
                'CMAKE_CXX_FLAGS',
                '-I{0}/rocblas/include'.format(incl)
            ))

        if self.spec.satisfies('@3.7.0:'):
            args.append(self.define_from_variant('OPTIMAL', 'optimal'))

        tgt = self.spec.variants['amdgpu_target'].value
        if tgt != 'auto':
            if '@:3.8.0' in self.spec:
                args.append(self.define('CMAKE_CXX_FLAGS',
                                        '--amdgpu-target={0}'.format(",".join(tgt))))
            else:
                args.append(self.define('AMDGPU_TARGETS', tgt))

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        if self.spec.satisfies('@4.5.0:'):
            args.append(self.define('ROCSOLVER_EMBED_FMT', 'ON'))

        return args

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)
