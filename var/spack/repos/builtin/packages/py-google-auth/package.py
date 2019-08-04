# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-google-auth
#
# You can edit this file again by typing:
#
#     spack edit py-google-auth
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class PyGoogleAuth(PythonPackage):
    """Google Auth Python Library """

    homepage = "https://github.com/googleapis/google-auth-library-python"
    url      = "https://github.com/googleapis/google-auth-library-python/archive/v1.5.1.tar.gz"

    version('1.6.3', '9e6d98c8e4f6ce899d6e5d416e7c372a')

    # Build dependencies
    depends_on('py-pkgconfig', type='build')
    depends_on('py-setuptools', type='build')
    depends_on('py-cachetools', type=('build', 'run'))
    depends_on('py-protobuf', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-rsa', type=('build', 'run'))
    depends_on('py-asn1crypto', type=('build', 'run'))

    phases = ['install']



