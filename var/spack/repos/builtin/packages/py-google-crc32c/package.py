# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGoogleCrc32c(PythonPackage):
    """This package wraps the google/crc32c hardware-based implementation
    of the CRC32C hashing algorithm."""

    homepage = "https://github.com/googleapis/python-crc32c"
    git      = "https://github.com/googleapis/python-crc32c"

    maintainers = ['marcusboden']

    version('1.3.0', tag='v1.3.0')

    depends_on('py-setuptools', type='build')
    depends_on('google-crc32c', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('CRC32C_INSTALL_PREFIX', self.spec['google-crc32c'].prefix)
