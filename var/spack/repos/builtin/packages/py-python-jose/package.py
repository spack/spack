# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonJose(PythonPackage):
    """The JavaScript Object Signing and Encryption(JOSE) implementation in
    Python."""

    homepage = "https://python-jose.readthedocs.io/en/latest"
    url      = "https://pypi.io/packages/source/p/python-jose/python-jose-3.0.1.tar.gz"

    version('3.0.1', sha256='ed7387f0f9af2ea0ddc441d83a6eb47a5909bd0c8a72ac3250e75afec2cc1371')

    depends_on('py-setuptools', type='build')

    depends_on('py-six', type='run')
    depends_on('py-rsa', type='run')
    depends_on('py-ecdsa', type='run')
