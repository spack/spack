# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class PyLaspy(PythonPackage):
    """Native Python ASPRS LAS read/write library."""

    homepage = "https://github.com/laspy/laspy"
    pypi     = "laspy/laspy-2.0.3.tar.gz"

    version('2.0.3', sha256='95c6367bc3a7c1e0d8dc118ae4a6b038bf9e8ad3e60741ecb8d59c36d32f822a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
