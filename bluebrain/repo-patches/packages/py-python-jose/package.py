# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyPythonJose(PythonPackage):
    """The JavaScript Object Signing and Encryption(JOSE) implementation in
    Python."""

    homepage = "https://python-jose.readthedocs.io/en/latest"
    pypi = "python-jose/python-jose-3.3.0.tar.gz"

    version('3.3.0', sha256='55779b5e6ad599c6336191246e95eb2293a9ddebd555f796a65f838f07e5d78a')

    depends_on('py-setuptools', type='build')
    depends_on('py-pytest-runner', type='build')

    depends_on('py-six', type=('build', 'run'))
    depends_on('py-rsa', type=('build', 'run'))
    depends_on('py-ecdsa@:0.14.999', type=('build', 'run'))
