# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit
    hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    pypi = "pre_commit/pre_commit-1.20.0.tar.gz"

    version('2.17.0', sha256='c1a8040ff15ad3d648c70cc3e55b93e4d2d5b687320955505587fd79bbaed06a')
    version('1.20.0', sha256='9f152687127ec90642a2cc3e4d9e1e6240c4eb153615cb02aa1ad41d331cbb6e')

    depends_on('python@2.7:2.8,3.5:', type=('build', 'run'))
    depends_on('python@3.6.1:', type=('build', 'run'), when="@2.1.0:")
    depends_on('py-setuptools', type='build')
    depends_on('py-aspy-yaml', type=('build', 'run'), when="@1")
    depends_on('py-cfgv@2.0.0:', type=('build', 'run'))
    depends_on('py-identify@1.0.0:', type=('build', 'run'))
    depends_on('py-nodeenv@0.11.1:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-pyyaml@5.1:', type=('build', 'run'), when="@2.1.0:")
    depends_on('py-six', type=('build', 'run'), when="@1")
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-virtualenv@15.2:', type=('build', 'run'))
    depends_on('py-virtualenv@20.0.8:', type=('build', 'run'), when="@2.4.0:")
    depends_on('py-futures', type=('build', 'run'), when='^python@:3.1')
    depends_on('py-importlib-metadata', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-importlib-resources@:5.2', type=('build', 'run'), when='^python@:3.6')
