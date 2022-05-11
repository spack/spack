# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyBottleneck(PythonPackage):
    """A collection of fast NumPy array functions written in Cython."""
    pypi = "Bottleneck/Bottleneck-1.0.0.tar.gz"

    version('1.3.2', sha256='20179f0b66359792ea283b69aa16366419132f3b6cf3adadc0c48e2e8118e573')
    version('1.3.1', sha256='451586370462cb623d6ad604a545d1e97fb51d2ab5252b1ac57350a83e494a28')
    version('1.3.0', sha256='9d7814c61c31f42cfb4f26e050c2659c88a198f1398a9714174ae78347aad737')
    version('1.2.1', sha256='6efcde5f830aed64feafca0359b51db0e184c72af8ba6675b4a99f263922eb36')
    version('1.0.0', sha256='8d9b7ad4fadf9648acc924a6ee522c7cb5b474e75faaad9d90dfd55e2805b495')

    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
