# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPreCommit(PythonPackage):
    """A framework for managing and maintaining multi-language pre-commit hooks."""

    homepage = "https://github.com/pre-commit/pre-commit"
    url      = "https://files.pythonhosted.org/packages/95/f1/dd0c0161dafa5ae8f73eef423a9898130db10d986a47a27e66625fe81178/pre_commit-1.14.4.tar.gz"

    version('1.14.4', sha256='d3d69c63ae7b7584c4b51446b0b583d454548f9df92575b2fe93a68ec800c4d3')

    depends_on('py-setuptools',  type='build')
    depends_on('py-aspy-yaml', type=('build', 'run'))
    depends_on('py-cfgv@1.4.0:', type=('build', 'run'))
    depends_on('py-futures', type=('build', 'run'), when='^python@2.7.0:2.7.999')
    depends_on('py-identify', type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'))
    depends_on('py-importlib-resources', type=('build', 'run'), when='^python@:3.7')
    depends_on('py-nodeenv@0.11.1:', type=('build', 'run'))
    depends_on('py-pyyaml', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))
    depends_on('py-toml', type=('build', 'run'))
    depends_on('py-virtualenv@15.2:', type=('build', 'run'))
