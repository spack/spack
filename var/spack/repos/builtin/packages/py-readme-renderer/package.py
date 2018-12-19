# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyReadmeRenderer(PythonPackage):
    """readme_renderer is a library for rendering "readme" descriptions
    for Warehouse."""

    homepage = "https://github.com/pypa/readme_renderer"
    url      = "https://pypi.io/packages/source/r/readme_renderer/readme_renderer-16.0.tar.gz"

    version('16.0', '70321cea986956bcf2deef9981569f39')

    depends_on('python@2.6:2.8,3.2:3.3')
    depends_on('py-setuptools', type='build')
    depends_on('py-bleach', type=('build', 'run'))
    depends_on('py-docutils@0.13.1:', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
