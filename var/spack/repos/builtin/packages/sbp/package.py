# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Sbp(CMakePackage):
    """Library providing an API for Piksi GNSS devices."""

    homepage = 'https://github.com/swift-nav/libsbp'
    git      = 'https://github.com/swift-nav/libsbp'

    maintainers = ['jayvdb']

    version('3.4.10', tag='v3.4.10', submodules=True)

    root_cmakelists_dir = 'c'

    def cmake_args(self):
        args = [
            self.define('BUILD_SHARED_LIBS', 'ON'),
            self.define('libsbp_ENABLE_TESTS', 'OFF'),
            self.define('libsbp_ENABLE_DOCS', 'OFF'),
        ]
        return args
