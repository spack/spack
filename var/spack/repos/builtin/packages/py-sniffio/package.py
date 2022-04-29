# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PySniffio(PythonPackage):
    """This is a tiny package whose only purpose is to let you detect which
    async library your code is running under."""

    homepage = "https://github.com/python-trio/sniffio"
    pypi = "sniffio/sniffio-1.1.0.tar.gz"

    version('1.2.0', sha256='c4666eecec1d3f50960c6bdf61ab7bc350648da6c126e3cf6898d8cd4ddcd3de')
    version('1.1.0', sha256='8e3810100f69fe0edd463d02ad407112542a11ffdc29f67db2bf3771afb87a21')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-contextvars@2.1:', when='^python@:3.6', type=('build', 'run'))
