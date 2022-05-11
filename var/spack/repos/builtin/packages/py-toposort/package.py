# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyToposort(PythonPackage):
    """Implements a topological sort algorithm."""

    pypi = 'toposort/toposort-1.6.tar.gz'

    maintainers = ['marcusboden']

    version('1.6', 'a7428f56ef844f5055bb9e9e44b343983773ae6dce0fe5b101e08e27ffbd50ac')

    depends_on('python@2.7:2.8,3.3:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
