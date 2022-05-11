# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Gotcha(CMakePackage):
    """C software library for shared library function wrapping,
    enables tools to intercept calls into shared libraries"""

    homepage = "https://github.com/LLNL/gotcha"
    git      = "https://github.com/LLNL/gotcha.git"

    tags = ['e4s']

    version('develop', branch='develop')
    version('master', branch='master')
    version('1.0.3', tag='1.0.3')
    version('1.0.2', tag='1.0.2')
    version('0.0.2', tag='0.0.2')

    variant('test', default=False, description='Build tests for Gotcha')
    patch(
        'https://github.com/LLNL/GOTCHA/commit/e82b4a1ecb634075d8f5334b796c888c86da0427.patch?full_index=1',
        sha256='3f05e61b00a1cd53ebc489e9ca5dc70b9767068bba30dba973cdbef9b14774e6',
        when='@0.0.2:1.0.2')

    def configure_args(self):
        return [
            self.define_from_variant('GOTCHA_ENABLE_TESTS', 'test')
        ]
