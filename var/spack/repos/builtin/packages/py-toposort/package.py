# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyToposort(PythonPackage):
    """Implements a topological sort algorithm
    """

    homepage = "https://bitbucket.org/ericvsmith/toposort"
    url      = "https://pypi.io/packages/source/t/toposort/toposort-1.5.tar.gz"

    version('1.5', sha256='dba5ae845296e3bf37b042c640870ffebcdeb8cd4df45adaa01d8c5476c557dd')

    depends_on('py-setuptools', type=('build', 'run'))
