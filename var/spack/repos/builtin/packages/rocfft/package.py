# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Rocfft(CMakePackage):
    """Radeon Open Compute FFT library"""

    homepage = "https://github.com/ROCmSoftwarePlatform/rocFFT/"
    git      = "https://github.com/ROCmSoftwarePlatform/rocFFT.git"
    url      = "https://github.com/ROCmSoftwarePlatform/rocfft/archive/rocm-4.5.0.tar.gz"

    maintainers = ['srekolam', 'arjun-raj-kuppala', 'haampie']

    version('4.5.2', sha256='2724118ca00b9e97ac9578fe0b7e64a82d86c4fb0246d0da88d8ddd9c608b1e1')
    version('4.5.0', sha256='045c1cf1737db6e7ee332c274dacdb565f99c976ed4cc5626a116878dc80a48c')
    version('4.3.1', sha256='fcdc4d12b93d967b6f992b4045da98433eabf2ee0ba84fc6b6f81e380584fbc9')
    version('4.3.0', sha256='cb5b8f62330bc61b17a3a2fd1500068ee05d48cb51797901dd259dbc84610478')
    version('4.2.0', sha256='db29c9067f0cfa98bddd3574f6aa7200cfc790cc6da352d19e4696c3f3982163')
    version('4.1.0', sha256='df23fcb05aae72557461ae3687be7e3b8b78be4132daf1aa9dc07339f4eba0cc', deprecated=True)
    version('4.0.0', sha256='d1d10d270f822e0bab64307313ef163ba449b058bf3352962bbb26d4f4db89d0', deprecated=True)
    version('3.10.0', sha256='9f57226aac7d9a0515e14a5a5b08a85e727de72b3f9c2177daf56749ac2c76ae', deprecated=True)
    version('3.9.0', sha256='9c9c0b7f09bab17250f5101d1605e7a61218eae828a3eb8fe048d607181294ce', deprecated=True)
    version('3.8.0', sha256='ed23009796e2ee7c43dcc24527f2d6b1d7a73dceac06c30384460098d2fe1556', deprecated=True)
    version('3.7.0', sha256='94462e4bd19c2c749fcf6903adbee66d4d3bd345c0246861ff8f40b9d08a6ead', deprecated=True)
    version('3.5.0', sha256='629f02cfecb7de5ad2517b6a8aac6ed4de60d3a9c620413c4d9db46081ac2c88', deprecated=True)

    variant('build_type', default='Release', values=("Release", "Debug", "RelWithDebInfo"), description='CMake build type')
    variant('amdgpu_target',
            values=spack.variant.any_combination_of(
                *ROCmPackage.amdgpu_targets_with_feature('xnack')))
    variant('amdgpu_target_sram_ecc',
            values=spack.variant.any_combination_of(
                *ROCmPackage.amdgpu_target_features['sramecc']),
            when='@3.9.0:4.0.0')

    depends_on('cmake@3:', type='build')

    for ver in ['3.5.0', '3.7.0', '3.8.0', '3.9.0', '3.10.0', '4.0.0', '4.1.0',
                '4.2.0', '4.3.0', '4.3.1', '4.5.0', '4.5.2']:
        depends_on('hip@' + ver,                      when='@' + ver)
        depends_on('rocm-cmake@' + ver, type='build', when='@' + ver)

    def setup_build_environment(self, env):
        env.set('CXX', self.spec['hip'].hipcc)

    def cmake_args(self):
        args = []

        tgt = self.spec.variants['amdgpu_target'].value

        if tgt[0] != 'none':
            if '@:3.8.0' in self.spec:
                args.append(self.define('CMAKE_CXX_FLAGS',
                                        '--amdgpu-target={0}'.format(",".join(tgt))))
            else:
                args.append(self.define('AMDGPU_TARGETS', ";".join(tgt)))

        # From version 3.9 and above we have AMDGPU_TARGETS_SRAM_ECC
        tgt_sram = self.spec.variants['amdgpu_target_sram_ecc'].value
        if tgt_sram[0] != 'none':
            args.append(self.define('AMDGPU_TARGETS_SRAM_ECC', ";".join(tgt_sram)))

        # See https://github.com/ROCmSoftwarePlatform/rocFFT/issues/322
        if self.spec.satisfies('^cmake@3.21.0:3.21.2'):
            args.append(self.define('__skip_rocmclang', 'ON'))

        return args
