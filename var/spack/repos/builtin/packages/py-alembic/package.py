# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlembic(PythonPackage):
    """Alembic is a database migrations tool."""

    homepage = "https://pypi.org/project/alembic/"
    url      = "https://pypi.io/packages/source/a/alembic/alembic-1.0.7.tar.gz"

    version('1.0.7', sha256='16505782b229007ae905ef9e0ae6e880fddafa406f086ac7d442c1aaf712f8c2')

    depends_on('py-setuptools', type='build')
