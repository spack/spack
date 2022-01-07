# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install py-google-crc32c
#
# You can edit this file again by typing:
#
#     spack edit py-google-crc32c
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGoogleCrc32c(PythonPackage):
    """This package wraps the google/crc32c hardware-based implementation of the CRC32C hashing algorithm."""

    homepage = "https://github.com/googleapis/python-crc32c"
    git      = "https://github.com/googleapis/python-crc32c"

    # maintainers = ['github_user1', 'github_user2']

    version('1.3.0', tag='v1.3.0')

    depends_on('py-setuptools', type='build')
    depends_on('google-crc32c', type=('build', 'run'))

    def setup_build_environment(self, env):
        env.set('CRC32C_INSTALL_PREFIX', self.spec['google-crc32c'].prefix)
