# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class PyPyrosar(PythonPackage):
    """A framework for large-scale SAR satellite data processing"""

    homepage = "https://github.com/johntruckenbrodt/pyroSAR"
    url      = "https://github.com/johntruckenbrodt/pyroSAR/archive/v0.8.tar.gz"

    version('0.11.1', sha256='cb4e045a25090de9d6da344d2320f86e51257ca230b7c7023c24d5b099df1523')
    version('0.11',   sha256='f0b833d957a853ec49889829f592535a6df759c89a38d204f76f2a024b40414a')
    version('0.10.1', sha256='9cbb1c4b9b31af54bae871890e6565ac27043b6ccc65a5482055adce7b6dd6e2')
    version('0.10',   sha256='22405de5b22615d582778361c5f50b70e0e57561dc451305797c930f2e3dea67')
    version('0.9.1',  sha256='8b966a0c579df60cd9e4fcc2f93ccb1a36f90a46529bcdd5a7c5170e52284958')
    version('0.9',    sha256='426e452584b96908ed6343523094ce20802cbe34912d6159e3c90566a87c0a0b')
    version('0.8', sha256='03f6d846afde85807a63f84b1fd25fe61e9a4cda93e9af7d44a67fd4b0b7dbc8')

    # python
    depends_on('py-setuptools', type='build')
    depends_on('py-progressbar2', type=('build', 'run'))
    depends_on('py-pathos@0.2.0:', type=('build', 'run'))
    depends_on('py-numpy@1.16.3', type=('build', 'run'))
    depends_on('py-scoop', type=('build', 'run'))
    depends_on('py-spatialist@0.2.8', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    # other
    depends_on('gdal+python', type=('build', 'link', 'run'))
