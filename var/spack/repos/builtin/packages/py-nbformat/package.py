# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyNbformat(PythonPackage):
    """The Jupyter Notebook format"""

    homepage = "https://github.com/jupyter/nbformat"
    url      = "https://github.com/jupyter/nbformat/archive/4.1.0.tar.gz"

    version('4.4.0', sha256='cfa7b2dbb81ab7a64492f09f2cb65d69a1d009fe5d6e18ee7bb94446b114ede3')
    version('4.1.0', sha256='751e77b58b66319be3977f86cc23a459763bded466a0113bbe39f137ec747872')
    version('4.0.1', sha256='5c46c21349f29379fa55bf19e4359afcd605fd4b5693a56807355874a2e87f78')
    version('4.0.0', sha256='f0dc6c6b47b9b0dcda1dfb02dd99c0818eb709571690a688d4e38a3129d2e95b')

    depends_on('py-ipython-genutils', type=('build', 'run'))
    depends_on('py-traitlets', type=('build', 'run'))
    depends_on('py-jsonschema', type=('build', 'run'))
    depends_on('py-jupyter-core', type=('build', 'run'))
