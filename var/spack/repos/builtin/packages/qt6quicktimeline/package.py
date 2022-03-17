# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qt6quicktimeline(CMakePackage):
    """Module for keyframe-based timeline construction."""

    url      = "https://github.com/qt/qtquicktimeline/archive/refs/tags/v6.2.3.tar.gz"

    maintainers = ['wdconinc', 'sethrj']

    version('6.2.3', sha256='bbb913398d8fb6b5b20993b5e02317de5c1e4b23a5357dd5d08a237ada6cc7e2')

    generator = 'Ninja'

    depends_on('cmake@3.16:', type='build')
    depends_on('ninja', type='build')
    depends_on("pkgconfig", type='build')
    depends_on("python", when='@5.7.0:', type='build')

    versions = ['6.2.3']
    for v in versions:
        depends_on('qt6base@{}'.format(v), when='@{}'.format(v))
        depends_on('qt6declarative@{}'.format(v), when='@{}'.format(v))

    def cmake_args(self):
        args = [
            # Qt components typically install cmake config files in a single prefix 
            self.define('QT_ADDITIONAL_PACKAGES_PREFIX_PATH',
                self.spec['qt6declarative'].prefix)
        ]
        return args
