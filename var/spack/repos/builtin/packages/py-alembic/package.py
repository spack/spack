# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAlembic(PythonPackage):
    """Alembic is a database migrations tool."""

    homepage = "https://pypi.org/project/alembic/"
    url      = "https://files.pythonhosted.org/packages/50/7a/17bc17b3f5b01ebd3af38d71a15baa33beb241ab280b6ad0977ae24ec208/alembic-1.0.6.tar.gz"

    version('1.0.6', sha256='35660f7e6159288e2be111126be148ef04cbf7306da73c8b8bd4400837bb08e3')

    depends_on('py-setuptools', type='build')
