# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPytestBdd(PythonPackage):
    """pytest-bdd implements a subset of the Gherkin language to enable
    automating project requirements testing and to facilitate behavioral
    driven development."""

    homepage = "https://github.com/pytest-dev/pytest-bdd"
    url      = "https://pypi.io/packages/source/p/pytest-bdd/pytest-bdd-4.1.0.tar.gz"

    version('4.1.0', sha256='304cd2b09923b838d0c2f08331d1f4236a14ef3594efa94e3bdae0f384d3fa5d')

    depends_on('py-setuptools', type='build')
    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-glob2', type=('build', 'run'))
    depends_on('py-mako', type=('build', 'run'))
    depends_on('py-parse', type=('build', 'run'))
    depends_on('py-parse-type', type=('build', 'run'))
    depends_on('py-py', type=('build', 'run'))
    depends_on('py-pytest@4.3:', type=('build', 'run'))
