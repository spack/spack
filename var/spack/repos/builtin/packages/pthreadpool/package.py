# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Pthreadpool(CMakePackage):
    """pthreadpool is a portable and efficient thread pool implementation."""

    homepage = "https://github.com/Maratyszcza/pthreadpool"
    git      = "https://github.com/Maratyszcza/pthreadpool.git"

    version('master', branch='master')

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')

    generator = 'Ninja'

    resource(
        name='fxdiv',
        git='https://github.com/Maratyszcza/FXdiv.git',
        branch='master'
    )
    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.10.0.zip',
        sha256='94c634d499558a76fa649edb13721dce6e98fb1e7018dfaeba3cd7a083945e91'
    )
    resource(
        name='googlebenchark',
        url='https://github.com/google/benchmark/archive/v1.5.3.zip',
        sha256='bdefa4b03c32d1a27bd50e37ca466d8127c1688d834800c38f3c587a396188ee'
    )

    def cmake_args(self):
        return [
            self.define('FXDIV_SOURCE_DIR',
                        join_path(self.stage.source_path, 'FXdiv')),
            self.define('GOOGLETEST_SOURCE_DIR',
                        join_path(self.stage.source_path, 'googletest-release-1.10.0')),
            self.define('GOOGLEBENCHMARK_SOURCE_DIR',
                        join_path(self.stage.source_path, 'benchmark-1.5.3')),
        ]
