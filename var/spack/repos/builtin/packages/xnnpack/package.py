# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Xnnpack(CMakePackage):
    """High-efficiency floating-point neural network inference operators for
    mobile, server, and Web"""

    homepage = "https://github.com/google/XNNPACK"
    git      = "https://github.com/google/XNNPACK.git"

    version('master', branch='master')
    version('2021-02-22', commit='55d53a4e7079d38e90acd75dd9e4f9e781d2da35')  # py-torch@1.8:1.9
    version('2020-03-23', commit='1b354636b5942826547055252f3b359b54acff95')  # py-torch@1.6:1.7
    version('2020-02-24', commit='7493bfb9d412e59529bcbced6a902d44cfa8ea1c')  # py-torch@1.5

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')

    generator = 'Ninja'

    resource(
        name='clog',
        url='https://github.com/pytorch/cpuinfo/archive/d5e37adf1406cf899d7d9ec1d317c47506ccb970.tar.gz',
        sha256='3f2dc1970f397a0e59db72f9fca6ff144b216895c1d606f6c94a507c1e53a025',
        destination='deps',
        placement='clog',
    )
    resource(
        name='cpuinfo',
        url='https://github.com/pytorch/cpuinfo/archive/5916273f79a21551890fd3d56fc5375a78d1598d.zip',
        sha256='2a160c527d3c58085ce260f34f9e2b161adc009b34186a2baf24e74376e89e6d',
        destination='deps',
        placement='cpuinfo',
    )
    resource(
        name='fp16',
        url='https://github.com/Maratyszcza/FP16/archive/3c54eacb74f6f5e39077300c5564156c424d77ba.zip',
        sha256='0d56bb92f649ec294dbccb13e04865e3c82933b6f6735d1d7145de45da700156',
        destination='deps',
        placement='fp16',
    )
    resource(
        name='fxdiv',
        url='https://github.com/Maratyszcza/FXdiv/archive/b408327ac2a15ec3e43352421954f5b1967701d1.zip',
        sha256='ab7dfb08829bee33dca38405d647868fb214ac685e379ec7ef2bebcd234cd44d',
        destination='deps',
        placement='fxdiv',
    )
    resource(
        name='pthreadpool',
        url='https://github.com/Maratyszcza/pthreadpool/archive/545ebe9f225aec6dca49109516fac02e973a3de2.zip',
        sha256='8461f6540ae9f777ce20d1c0d1d249e5e61c438744fb390c0c6f91940aa69ea3',
        destination='deps',
        placement='pthreadpool',
    )
    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/5a509dbd2e5a6c694116e329c5a20dc190653724.zip',
        sha256='fcfac631041fce253eba4fc014c28fd620e33e3758f64f8ed5487cc3e1840e3d',
        destination='deps',
        placement='googletest',
    )
    resource(
        name='googlebenchmark',
        url='https://github.com/google/benchmark/archive/v1.4.1.zip',
        sha256='61ae07eb5d4a0b02753419eb17a82b7d322786bb36ab62bd3df331a4d47c00a7',
        destination='deps',
        placement='googlebenchmark',
    )
    resource(
        name='psimd',
        git='https://github.com/Maratyszcza/psimd.git',
        branch='master',
        destination='deps',
        placement='psimd',
    )

    def cmake_args(self):
        # TODO: XNNPACK has a XNNPACK_USE_SYSTEM_LIBS option, but it seems to be broken
        # See https://github.com/google/XNNPACK/issues/1543
        return [
            self.define('CLOG_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'clog')),
            self.define('CPUINFO_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'cpuinfo')),
            self.define('FP16_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'fp16')),
            self.define('FXDIV_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'fxdiv')),
            self.define('PTHREADPOOL_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'pthreadpool')),
            self.define('GOOGLETEST_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googletest')),
            self.define('GOOGLEBENCHMARK_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googlebenchmark')),
            self.define('PSIMD_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'psimd')),
            self.define('XNNPACK_BUILD_TESTS', self.run_tests),
            self.define('XNNPACK_BUILD_BENCHMARKS', self.run_tests),
        ]
