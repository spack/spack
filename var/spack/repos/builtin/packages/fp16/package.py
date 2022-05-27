# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fp16(CMakePackage):
    """FP16 is a header-only library for
    conversion to/from half-precision floating point formats"""

    homepage = "https://github.com/Maratyszcza/FP16/"
    git      = "https://github.com/Maratyszcza/FP16.git"

    version('master', branch='master')
    version('2020-05-14', commit='4dfe081cf6bcd15db339cf2680b9281b8451eeb3')  # py-torch@1.5:1.9
    version('2018-11-28', commit='febbb1c163726b5db24bed55cc9dc42529068997')  # py-torch@1.1:1.4
    version('2018-10-10', commit='34d4bf01bbf7376f2baa71b8fa148b18524d45cf')  # py-torch@1.0
    version('2018-02-25', commit='43d6d17df48ebf622587e7ed9472ea76573799b9')  # py-torch@:0.4

    depends_on('cmake@2.8.12:', type='build')
    depends_on('ninja', type='build')

    generator = 'Ninja'

    resource(
        name='psimd',
        git='https://github.com/Maratyszcza/psimd.git',
        branch='master',
        destination='deps',
        placement='psimd',
    )
    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.8.0.zip',
        sha256='f3ed3b58511efd272eb074a3a6d6fb79d7c2e6a0e374323d1e6bcbcc1ef141bf',
        destination='deps',
        placement='googletest',
    )
    resource(
        name='googlebenchmark',
        url='https://github.com/google/benchmark/archive/v1.2.0.zip',
        sha256='cc463b28cb3701a35c0855fbcefb75b29068443f1952b64dd5f4f669272e95ea',
        destination='deps',
        placement='googlebenchmark',
    )

    def cmake_args(self):
        return [
            self.define('PSIMD_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'psimd')),
            self.define('GOOGLETEST_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googletest')),
            self.define('GOOGLEBENCHMARK_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googlebenchmark')),
            self.define('FP16_BUILD_TESTS', self.run_tests),
            self.define('FP16_BUILD_BENCHMARKS', self.run_tests),
        ]
