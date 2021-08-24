# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyMeshio(PythonPackage):
    """MeshIO is a Python library to read and write many mesh formats."""

    homepage = "https://github.com/nschloe/meshio"
    url      = "https://github.com/nschloe/meshio/archive/refs/tags/5.0.0.tar.gz"

    version('5.0.0', sha256='68c221872226d504296f94294b61f278cc838dd42dfcb08708398cf30790c38b')

    # MeshIO uses a setup.cfg/pyproject.toml structure, which spack doesn't yet handle.
    # This patch adds a small setup.py file that spack can call.
    patch('setup.patch')

    depends_on('python@3.7:')
    depends_on('py-numpy')
