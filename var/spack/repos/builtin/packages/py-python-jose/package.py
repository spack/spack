# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonJose(PythonPackage):
    """The JavaScript Object Signing and Encryption(JOSE) implementation in Python."""

    homepage = "https://python-jose.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-jose/python-jose-3.0.1.tar.gz"

    version('3.0.1', 'f5f921985e5259559bf6ab9e60b1704e')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
    depends_on('py-rsa', type='run')
    depends_on('py-ecdsa', type='run')
