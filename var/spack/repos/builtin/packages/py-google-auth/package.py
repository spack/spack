# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyGoogleAuth(PythonPackage):
    """This library simplifies using Google's various server-to-server
    authentication mechanisms to access Google APIs."""

    homepage = "https://github.com/GoogleCloudPlatform/google-auth-library-python"
    pypi = "google-auth/google-auth-1.6.3.tar.gz"

    version('2.3.2', sha256='2dc5218ee1192f9d67147cece18f47a929a9ef746cb69c50ab5ff5cfc983647b')
    version('1.6.3', sha256='0f7c6a64927d34c1a474da92cfc59e552a5d3b940d3266606c6a28b72888b9e4')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('python@3.6:', type=('build', 'run'), when='@1.35:')
    depends_on('python@2.7:2.8,3.6:', type=('build', 'run'), when='@1.24:')
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools@40.3.0:', type='build', when='@2.3.2:')
    depends_on('py-pyasn1-modules@0.2.1:', type=('build', 'run'))
    depends_on('py-rsa@3.1.4:', type=('build', 'run'))
    depends_on('py-rsa@3.1.4:4', type=('build', 'run'), when='@2.3.2 ^python@3.6:')
    depends_on('py-rsa@:4.5', type=('build', 'run'), when='@2.3.2 ^python@:3.5')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-cachetools@2.0.0:', type=('build', 'run'))
    depends_on('py-cachetools@2.0.0:4', type=('build', 'run'), when='@2.3.2:')
    depends_on('py-enum34@1.1.10:', type=('build', 'run'), when='@2.3.2: ^python@:3.3')
