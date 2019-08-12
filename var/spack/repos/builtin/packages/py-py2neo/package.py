# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPy2neo(PythonPackage):
    """Py2neo is a client library and toolkit for working with Neo4j from
    within Python applications and from the command line."""

    homepage = "http://py2neo.org/"
    url      = "https://github.com/nigelsmall/py2neo/archive/py2neo-2.0.8.tar.gz"

    version('2.0.8', 'e3ec5172a9e006515ef4155688a05a55')
    version('2.0.7', '4cfbc5b7dfd7757f3d2e324805faa639')
    version('2.0.6', '53e4cdb1a95fbae501c66e541d5f4929')
    version('2.0.5', '143b1f9c0aa22faf170c1b9f84c7343b')
    version('2.0.4', 'b3f7efd3344dc3f66db4eda11e5899f7')

    depends_on("py-setuptools", type='build')
