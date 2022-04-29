# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyFormulaic(PythonPackage):
    """Formulaic is a high-performance implementation of Wilkinson formulas
    for Python."""

    homepage = "https://github.com/matthewwardrop/formulaic"
    pypi = "formulaic/formulaic-0.2.4.tar.gz"

    version('0.2.4', sha256='15b71ea8972fb451f80684203cddd49620fc9ed5c2e35f31e0874e9c41910d1a')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setupmeta', type='build')
    depends_on('py-astor', type=('build', 'run'))
    depends_on('py-interface-meta@1.2:', type=('build', 'run'))
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-pandas', type=('build', 'run'))
    depends_on('py-scipy', type=('build', 'run'))
    depends_on('py-wrapt', type=('build', 'run'))
