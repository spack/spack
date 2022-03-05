# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
from spack import *


class PyMariadb(PythonPackage):
    """A module for connecting to mariaDB databases"""

    homepage = "https://github.com/mariadb-corporation/mariadb-connector-python"
    pypi = "mariadb/mariadb-1.0.10.zip"

    version('1.0.10', sha256='79028ba6051173dad1ad0be7518389cab70239f92b4ff8b8813dae55c3f2c53d')

    depends_on('py-setuptools', type='build')
    depends_on('mariadb-c-client', type=('build', 'run'))
