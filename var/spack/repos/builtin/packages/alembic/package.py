# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Alembic(CMakePackage):
    """Alembic is an open computer graphics interchange
    framework. Alembic distills complex, animated scenes into a
    non-procedural, application-independent set of baked
    geometric results."""

    homepage = "https://www.alembic.io"
    url      = "https://github.com/alembic/alembic/archive/1.7.16.tar.gz"

    version('1.7.16', sha256='2529586c89459af34d27a36ab114ad1d43dafd44061e65cfcfc73b7457379e7c')

    # FIXME: Add dependencies if required.
    # depends_on('foo')

    def cmake_args(self):
        # FIXME: Add arguments other than
        # FIXME: CMAKE_INSTALL_PREFIX and CMAKE_BUILD_TYPE
        # FIXME: If not needed delete this function
        args = []
        return args
