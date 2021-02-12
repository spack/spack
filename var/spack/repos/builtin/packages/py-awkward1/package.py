# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAwkward1(PythonPackage):
    """ROOT I/O in pure Python and NumPy."""

    git = "https://github.com/scikit-hep/awkward-1.0.git"
    url = "https://github.com/scikit-hep/awkward-1.0/archive/0.3.1.tar.gz"
    homepage = "https://awkward-array.org"

    maintainers = ['vvolkl']

    version('1.1.2', sha256='626e3a6a2a92dd67abc8692b1ebfa1b447b9594352d6ce8c86c37d7299dc4602')
    version('1.1.1', sha256='867da94bef3360e34ae3b7244e2acdbe3749d3338b00ed1335cce5e6fe06ccc5')
    version('1.1.0', sha256='ec1e6601546c5968f3cce7276d5af23ccc8cada960e6008198d0ebcc6ecd52a8')
    version('1.0.2', sha256='af20eac75c9b05a1469383f7935bd273df33457d1ab3ef3f3edd677a68f5c71c')
    version('0.3.1', sha256='7126d9feab8828b0b4f4c6dbc9e28c269a91e28eef4a6033d7ebb5db21f1dab3')

    patch('pybind11.patch')

    depends_on('py-setuptools', type='build')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-numpy@1.13.1:')
    depends_on('py-pybind11')
    depends_on('rapidjson')
    depends_on('cmake', type='build')
