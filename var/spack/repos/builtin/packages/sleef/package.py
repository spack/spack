# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sleef(CMakePackage):
    """SIMD Library for Evaluating Elementary Functions, vectorized libm and DFT."""

    homepage = "https://sleef.org"
    url      = "https://github.com/shibatch/sleef/archive/3.2.tar.gz"
    git      = "https://github.com/shibatch/sleef.git"

    version('master', branch='master')
    version('3.5.1_2020-12-22', commit='e0a003ee838b75d11763aa9c3ef17bf71a725bff')  # py-torch@1.8:1.9
    version('3.5.1', sha256='415ee9b1bcc5816989d3d4d92afd0cd3f9ee89cbd5a33eb008e69751e40438ab', preferred=True)
    version('3.4.0_2019-07-30', commit='7f523de651585fe25cade462efccca647dcc8d02')  # py-torch@1.3:1.7
    version('3.4.0_2019-05-13', commit='9b249c53a80343cc1a394ca961d7d5696ea76409',  # py-torch@1.2
            git='https://github.com/zdevito/sleef.git')
    version('3.3.1_2018-12-09', commit='191f655caa25526ae226cf88dd2529265176014a',  # py-torch@1.1
            git='https://github.com/zdevito/sleef.git')
    version('3.2_2018-05-09', commit='6ff7a135a1e31979d1e1844a2e7171dfbd34f54f')  # py-torch@0.4.1:1.0
    version('3.2', sha256='3130c5966e204e6d6a3ace81e543d12b5b21f60897f1c185bfa587c1bd77bee2')

    # Some versions have ICE when building RelWithDebInfo with GCC 7
    # See https://github.com/shibatch/sleef/issues/234
    # See https://github.com/pytorch/pytorch/issues/26892
    # See https://github.com/pytorch/pytorch/pull/26993
    variant('build_type', default='Release',
            description='CMake build type',
            values=('Debug', 'Release', 'RelWithDebInfo', 'MinSizeRel'))

    depends_on('cmake@3.4.3:', type='build')
    depends_on('ninja', type='build')

    generator = 'Ninja'

    def cmake_args(self):
        return [
            self.define('DISABLE_FFTW', True),
            self.define('DISABLE_MPFR', True),
            self.define('DISABLE_SSL', True),
        ]
