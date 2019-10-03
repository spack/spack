# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyImportlibMetadata(PythonPackage):
    """Read metadata from Python packages."""

    homepage = "http://importlib-metadata.readthedocs.io/"
    url      = "https://pypi.io/packages/source/i/importlib_metadata/importlib_metadata-0.19.tar.gz"

    version('0.19', sha256='23d3d873e008a513952355379d93cbcab874c58f4f034ff657c7a87422fa64e8')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-zipp@0.5:', type=('build', 'run'))
    depends_on('py-pathlib2', when='^python@:3.3', type=('build', 'run'))
    depends_on('py-contextlib2', when='^python@:2.8', type=('build', 'run'))
    depends_on('py-configparser@3.5:', when='^python@:2.8', type=('build', 'run'))
