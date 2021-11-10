# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonJose(PythonPackage):
    """The JavaScript Object Signing and Encryption(JOSE) implementation in
    Python."""

    homepage = "https://python-jose.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-jose/python-jose-3.2.0.tar.gz"

    version('3.2.0', sha256='4e4192402e100b5fb09de5a8ea6bcc39c36ad4526341c123d401e2561720335b')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')

    depends_on('py-six', type=('build', 'run'))
    depends_on('py-rsa', type=('build', 'run'))
    depends_on('py-ecdsa@:0.14.999', type=('build', 'run'))
