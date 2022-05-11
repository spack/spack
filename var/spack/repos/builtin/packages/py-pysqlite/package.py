# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class PyPysqlite(PythonPackage):
    """Python DB-API module for SQLite 3."""

    homepage = "https://github.com/ghaering/pysqlite"
    pypi = "pysqlite/pysqlite-2.8.3.tar.gz"

    version('2.8.3', sha256='17d3335863e8cf8392eea71add33dab3f96d060666fe68ab7382469d307f4490')

    # pysqlite is built into Python3
    depends_on('python@2.7.0:2.7', type=('build', 'run'))
    # pip silently replaces distutils with setuptools
    depends_on('py-setuptools', type='build')
    depends_on('sqlite', type=('build', 'run'))
