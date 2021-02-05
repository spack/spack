# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyHyperopt(PythonPackage):
    """Hyperopt is a Python library for serial and parallel optimization over
    awkward search spaces, which may include real-valued, discrete, and
    conditional dimensions."""

    homepage = "http://hyperopt.github.io/hyperopt/"
    pypi     = "hyperopt/hyperopt-0.2.5.tar.gz"
    url      = "https://github.com/hyperopt/hyperopt/archive/0.2.5.zip"

    version('0.2.5', sha256='2e3484be226ed1339e003553f0328b440cbf9c577b92553409fb160ecb671406')
    version('0.2.4', sha256='acf58881152269ae7bd9a9b834449221baf298c5c95a4d2331c626d4753a4721')
    version('0.2.2', sha256='4dd384d3ac18e4f8165321d6576ade703513bca43c9c51d6a00bc6fba747811e')
    version('0.2.1', sha256='a6817b88b7c4807734c5729380bf0058b582d0efeacc8007d37244ff6e8c28d9')
    version('0.2',   sha256='3419179f71e962d4c9ecd81ad06f2918a604b060fe07189ef65417274807d054')

    depends_on('python@2.7:',       type=('build', 'run'))
    depends_on('py-setuptools',     type='build')
    depends_on('py-numpy',          type=('build', 'run'))
    depends_on('py-scipy',          type=('build', 'run'))
    depends_on('py-six',            type=('build', 'run'))
    depends_on('py-networkx@2.2:',  type=('build', 'run'))
    depends_on('py-future',         type=('build', 'run'))
    depends_on('py-tqdm',           type=('build', 'run'))
    depends_on('py-cloudpickle',    type=('build', 'run'))
    depends_on('py-pyspark',        type=('build', 'run'))
    depends_on('py-pymongo',        type=('build', 'run'))
    depends_on('py-scikit-learn',   type=('build', 'run'))
