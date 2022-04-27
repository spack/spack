# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyColossalai(PythonPackage):
    """An integrated large-scale model training system with efficient
    parallelization techniques."""

    homepage = "https://pypi.org/project/colossalai"
    pypi     = "colossalai/colossalai-0.1.0.tar.gz"

    version('0.1.3', sha256='f25ffd313e62b2cb8f97c57f25fafb0e9f59ec7bd1d1bf6e8d8483f9b0082d33')
    version('0.1.2', sha256='3f3c0afc4871aa65405c59e7c08601c0c58e49f9990e6411ee797f173e2ffa52')
    version('0.1.1', sha256='7463c11abb3c33446411d8cde7dfce37d0c7d6b559f7c04c40d59ed24c1ac359')
    version('0.1.0', sha256='3e3dce61f577b8bb3b1ce3c01d7cf7dfd9ef1a2c0a2d8a46bc510ed750d90f24')
    version('0.0.2', sha256='d1c4f47c80983f0e526aa5b4ba91452d4b0abf145c829205d4e8c1b9e0ba74fc')

    depends_on('python@3.7:', type=('build', 'run'))
