# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Gotcha(CMakePackage):
    """C software library for shared library function wrapping,
    enables tools to intercept calls into shared libraries"""

    homepage = "http://github.com/LLNL/gotcha"
    git      = "https://github.com/LLNL/gotcha.git"

    version('develop', branch='develop')
    version('master', branch='master')
    version('1.0.2', tag='1.0.2')
    version('0.0.2', tag='0.0.2')

    variant('test', default=False, description='Build tests for Gotcha')
    patch('arm.patch', when='@1.0.2')

    def configure_args(self):
        spec = self.spec
        return [
            '-DGOTCHA_ENABLE_TESTS=%s' % ('ON' if '+test' in spec else 'OFF')
        ]
