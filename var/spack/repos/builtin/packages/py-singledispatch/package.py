# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PySingledispatch(PythonPackage):
    """This library brings functools.singledispatch to Python 2.6-3.3."""

    pypi = "singledispatch/singledispatch-3.4.0.3.tar.gz"

    version('3.7.0', sha256='c1a4d5c1da310c3fd8fccfb8d4e1cb7df076148fd5d858a819e37fffe44f3092')
    version('3.4.0.3', sha256='5b06af87df13818d14f08a028e42f566640aef80805c3b50c5056b086e3c2b9c')

    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-setuptools@42:', type='build', when='@3.7:')
    depends_on('py-setuptools-scm@3.4.1: +toml', type='build', when='@3.7:')
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-ordereddict', when="^python@:2.6", type=('build', 'run'))
