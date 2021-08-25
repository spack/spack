# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMeshio(PythonPackage):
    """MeshIO is a Python library to read and write many mesh formats."""

    homepage = "https://github.com/nschloe/meshio"
    pypi = "meshio/meshio-5.0.0.tar.gz"

    version('5.0.0', sha256='f6327c06d6171d30e0991d3dcb048751035f9cfac1f19e2444971275fd971188')

    # MeshIO uses a setup.cfg/pyproject.toml structure, which spack doesn't yet handle.
    # This patch adds a small setup.py file that spack can call.
    patch('setup.patch')

    depends_on('python@3.7:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-numpy', type=('build', 'run'))
    depends_on('py-importlib-metadata', when='^python@:3.7', type=('build', 'run'))
