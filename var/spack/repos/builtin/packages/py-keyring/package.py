# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyKeyring(PythonPackage):
    """The Python keyring library provides an easy way to access the system keyring
    service from python. It can be used in any application that needs safe password
    storage."""

    homepage = "https://github.com/jaraco/keyring"
    pypi     = "keyring/keyring-23.0.1.tar.gz"

    version('23.2.1', sha256='6334aee6073db2fb1f30892697b1730105b5e9a77ce7e61fca6b435225493efe')
    version('23.2.0', sha256='1e1970dcecde00c59ff6033d69cee3b283cd0d7cbad78b0dc4cdd15c8a28bcf8')
    version('23.1.0', sha256='b7e0156667f5dcc73c1f63a518005cd18a4eb23fe77321194fefcc03748b21a4')
    version('23.0.1', sha256='045703609dd3fccfcdb27da201684278823b72af515aedec1a8515719a038cb8')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools@42:', type='build')
    depends_on('py-setuptools@56:', type='build', when='@23.1.0:')
    depends_on('py-setuptools-scm@3.4.1:+toml', type='build')
    depends_on('py-importlib-metadata@3.6:', type=('build', 'run'))
    depends_on('py-secretstorage@3.2:', type=('build', 'run'), when='platform=linux')
    depends_on('py-jeepney@0.4.2:', type=('build', 'run'), when='platform=linux')

    # TODO: additional dependency on pywin32-ctypes required for Windows
