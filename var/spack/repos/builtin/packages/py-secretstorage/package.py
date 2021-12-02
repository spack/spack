# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySecretstorage(PythonPackage):
    """Python bindings to FreeDesktop.org Secret Service API."""

    homepage = "https://github.com/mitya57/secretstorage"
    pypi = "SecretStorage/SecretStorage-3.1.2.tar.gz"

    version('3.3.1', sha256='fd666c51a6bf200643495a04abb261f83229dcb6fd8472ec393df7ffc8b6f195')
    version('3.1.2', sha256='15da8a989b65498e29be338b3b279965f1b8f09b9668bd8010da183024c8bff6')

    depends_on('python@3.6:', when='@3.3:', type=('build', 'run'))
    depends_on('python@3.5:', when='@:3.2', type=('build', 'run'))
    depends_on('py-setuptools@30.3:', type='build')
    depends_on('py-cryptography@2.0:', when='@3.2:', type=('build', 'run'))
    depends_on('py-cryptography', when='@:3.1', type=('build', 'run'))
    depends_on('py-jeepney@0.6:', when='@3.3:', type=('build', 'run'))
    depends_on('py-jeepney@0.4.2:', when='@:3.2', type=('build', 'run'))
