# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Cpuinfo(CMakePackage):
    """cpuinfo is a library to detect essential
    for performance optimization information about host CPU."""

    homepage = "https://github.com/Maratyszcza/cpuinfo/"
    git      = "https://github.com/Maratyszcza/cpuinfo.git"

    version('master', branch='master')

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')

    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.10.0.zip',
        sha256='94c634d499558a76fa649edb13721dce6e98fb1e7018dfaeba3cd7a083945e91',
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

    generator = 'Ninja'

    def cmake_args(self):
        return [
            self.define('GOOGLETEST_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googletest')),
            self.define('GOOGLEBENCHMARK_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googlebenchmark')),
        ]
