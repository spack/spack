# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAiodns(PythonPackage):
    """Simple DNS resolver for asyncio.It provides a simple way for
    doing asynchronous DNS resolutions using pycares."""

    homepage = "https://pypi.org/project/aiodns/"
    url      = "https://github.com/saghul/aiodns/archive/aiodns-2.0.0.tar.gz"

    version('2.0.0', sha256='f5f9f066d34dbf6120ec4a9357ba322313721a5fe7e9f0dec64d29df643e699c')
    version('1.2.0', sha256='10fbdd52ba0e5523e12fb863f892fc8ea7c6da2fa42f12c748e3b704464c6824')
    version('1.1.1', sha256='a91cd89880a163005da698da5f1779ebe0ba752a927d4244c0dd99c34320fb7d')

    depends_on('py-setuptools', type='build')
    depends_on('python@:3.6.99', type=('build', 'run'))
    depends_on('py-typing', type=('build', 'run'))
    depends_on('py-pycares@3.0.0:', type=('build', 'run'))
