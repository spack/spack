# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fxdiv(CMakePackage):
    """Header-only library for division via fixed-point multiplication by inverse."""

    homepage = "https://github.com/Maratyszcza/FXdiv"
    git      = "https://github.com/Maratyszcza/FXdiv.git"

    version('master', branch='master')
    version('2020-04-17', commit='b408327ac2a15ec3e43352421954f5b1967701d1')  # py-torch@1.6:1.9
    version('2018-11-16', commit='b742d1143724d646cd0f914646f1240eacf5bd73')  # py-torch@1.0:1.5
    version('2018-02-24', commit='811b482bcd9e8d98ad80c6c78d5302bb830184b0')  # py-torch@0.4

    depends_on('cmake@3.5:', type='build')
    depends_on('ninja', type='build')
    depends_on('python', type='build')

    generator = 'Ninja'

    resource(
        name='googletest',
        url='https://github.com/google/googletest/archive/release-1.10.0.zip',
        sha256='94c634d499558a76fa649edb13721dce6e98fb1e7018dfaeba3cd7a083945e91',
        destination='deps',
        placement='googletest',
    )
    resource(
        name='googlebenchmark',
        url='https://github.com/google/benchmark/archive/v1.5.0.zip',
        sha256='2d22dd3758afee43842bb504af1a8385cccb3ee1f164824e4837c1c1b04d92a0',
        destination='deps',
        placement='googlebenchmark',
    )

    def cmake_args(self):
        return [
            self.define('GOOGLETEST_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googletest')),
            self.define('GOOGLEBENCHMARK_SOURCE_DIR',
                        join_path(self.stage.source_path, 'deps', 'googlebenchmark')),
        ]
