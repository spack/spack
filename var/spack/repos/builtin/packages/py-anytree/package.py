# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyAnytree(PythonPackage):
    """Python tree data library - lightweight and extensible Tree data structure."""

    homepage    = 'https://github.com/c0fec0de/anytree'
    pypi        = 'anytree/anytree-2.8.0.tar.gz'
    maintainers = ['bernhardkaindl']

    version('2.8.0', sha256='3f0f93f355a91bc3e6245319bf4c1d50e3416cc7a35cc1133c1ff38306bbccab')

    depends_on('py-setuptools', type='build')
    depends_on('py-six@1.9.0:', type=('build', 'run'))
    depends_on('py-ordereddict', when='^python@:2.6', type=('build', 'run'))
