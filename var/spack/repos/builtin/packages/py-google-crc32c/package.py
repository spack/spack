# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyGoogleCrc32c(PythonPackage):
    """This package wraps the google/crc32c hardware-based implementation
    of the CRC32C hashing algorithm."""

    homepage = "https://github.com/googleapis/python-crc32c"
    pypi = "google-crc32c/google-crc32c-1.3.0.tar.gz"

    maintainers = ['marcusboden']

    version('1.3.0', '276de6273eb074a35bc598f8efbc00c7869c5cf2e29c90748fccc8c898c244df')

    depends_on('py-setuptools', type='build')
    depends_on('google-crc32c', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('CRC32C_INSTALL_PREFIX', self.spec['google-crc32c'].prefix)
