# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


class PySqlalchemyStubs(PythonPackage):
    """
    SQLAlchemy stubs and mypy plugin
    """

    homepage = "https://github.com/dropbox/sqlalchemy-stubs"
    pypi     = "sqlalchemy-stubs/sqlalchemy-stubs-0.4.tar.gz"

    version('0.4', sha256='c665d6dd4482ef642f01027fa06c3d5e91befabb219dc71fc2a09e7d7695f7ae')

    depends_on('python@3.4:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
