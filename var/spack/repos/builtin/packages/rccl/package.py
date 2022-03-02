# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rccl(CMakePackage):
    """RCCL (pronounced "Rickle") is a stand-alone library
    of standard collective communication routines for GPUs,
    implementing all-reduce, all-gather, reduce, broadcast,
    and reduce-scatter."""

    homepage = "https://github.com/ROCmSoftwarePlatform/rccl"
    git      = "https://github.com/ROCmSoftwarePlatform/rccl.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rccl/archive/rocm-4.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala']
    version('master', branch='develop')
    version('4.5.2', sha256='36de0d3f3ffad491758d89c208ef72c5be5e0db766053a9c766e9c5c6a33a487')
    version('4.5.0', sha256='f806f9f65c490abddc562cb4812e12701582bbb449e41cc4797d00e0dedf084e')
    version('4.3.1', sha256='c5db71423dc654e8d2c3111e142e65c89436bc636827d95d41a09a87f44fe246')
    version('4.3.0', sha256='b5231d8c5ab034a583feceebcef68d0cc0b05ec5a683f802fc7747c89f27d5f6')
    version('4.2.0', sha256='2829fae40ebc1d8be201856d2193a941c87e9cf38dca0a2f4414e675c1742f20')
    version('4.1.0', sha256='88ec9b43c31cb054fe6aa28bcc0f4b510213635268f951939d6980eee5bb3680', deprecated=True)
    version('4.0.0', sha256='0632a15b3d6b5981c05377cf4aeb51546f4c4901fd7c37fb0c98071851ad531a', deprecated=True)
    version('3.10.0', sha256='d9dd0b0d8b9d056fc5e6c7b814520800190952acd30dac3a7c462c4cb6f42bb3', deprecated=True)
    version('3.9.0', sha256='ff9d03154d668093309ff814a33788f2cc093b3c627e78e42ae246e6017408b0', deprecated=True)
    version('3.8.0', sha256='0b6676d06bdb1f65d511a95db9f842a3443def83d75759dfdf812b5e62d8c910', deprecated=True)
    version('3.7.0', sha256='8273878ff71aac2e7adf5cc8562d2933034c6c6b3652f88fbe3cd4f2691036e3', deprecated=True)
    version('3.5.0', sha256='290b57a66758dce47d0bfff3f5f8317df24764e858af67f60ddcdcadb9337253', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')

    patch('0001-Fix-numactl-path-issue.patch', when='@3.7.0:4.3.2')
    patch('0002-Fix-numactl-rocm-smi-path-issue.patch', when='@4.5.0:')

    depends_on('cmake@3:', type='build')
    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2', 'master']:
        depends_on('rocm-cmake@' + ver,   type='build', when='@' + ver)
        depends_on('hip@' + ver,                        when='@' + ver)
        depends_on('comgr@' + ver,                      when='@' + ver)
        depends_on('hsa-rocr-dev@' + ver,               when='@' + ver)

    for ver in ['3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0', '4.2.0',
                '4.3.0', '4.3.1', '4.5.0', '4.5.2', 'master']:
        depends_on('numactl@2:', when='@' + ver)
    for ver in ['4.5.0', '4.5.2', 'master']:
        depends_on('rocm-smi-lib@' + ver, when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = []
        if '@3.7.0:' in self.spec:
            args.append(self.define(
                'NUMACTL_DIR',
                self.spec['numactl'].prefix
            ))

        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        if self.spec.satisfies('@4.5.0:'):
            args.append(self.define('ROCM_SMI_DIR', self.spec['rocm-smi-lib'].prefix))
        return args
