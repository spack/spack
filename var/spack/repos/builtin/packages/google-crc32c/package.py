# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class GoogleCrc32c(CMakePackage):
    """CRC32C implementation with support for CPU-specific acceleration instructions."""

    homepage = "https://github.com/google/crc32c"
    git      = "https://github.com/google/crc32c"

    maintainers = ['marcusboden']

    version('1.1.2', tag='1.1.2')

    depends_on('cmake@3.1:', type='build')

    def cmake_args(self):
        args = [
            self.define('CRC32C_BUILD_TESTS', False),
            self.define('CRC32C_BUILD_BENCHMARKS', False),
            self.define('CRC32C_USE_GLOG', False),
            self.define('BUILD_SHARED_LIBS', True),
        ]
        return args
