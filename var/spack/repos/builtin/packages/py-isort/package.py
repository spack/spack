# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class PyIsort(PythonPackage):
    """A Python utility / library to sort Python imports."""

    homepage = "https://github.com/timothycrosley/isort"
    pypi = "isort/isort-4.2.15.tar.gz"

    version('5.9.3', sha256='9c2ea1e62d871267b78307fe511c0838ba0da28698c5732d54e2790bf3ba9899')
    version('5.9.1', sha256='83510593e07e433b77bd5bff0f6f607dbafa06d1a89022616f02d8b699cfcd56')
    version('4.3.20', sha256='c40744b6bc5162bbb39c1257fe298b7a393861d50978b565f3ccd9cb9de0182a')
    version('4.2.15', sha256='79f46172d3a4e2e53e7016e663cc7a8b538bec525c36675fcfd2767df30b3983')

    variant('colors', default=False, description='Install colorama for --color support')

    depends_on('python@3.6.1:3', type=('build', 'run'), when='@5:')
    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'), when='@4.3:')
    depends_on('python@2.6:2.8,3.3:', type=('build', 'run'))
    depends_on('py-poetry-core@1:', type='build')
    depends_on('py-futures', type=('build', 'run'), when='@4.3:4 ^python@:3.1')
    depends_on('py-backports-functools-lru-cache', type=('build', 'run'), when='@4.3.10:4 ^python@:3.1')
    depends_on('py-colorama@0.4.3:0.4', type=('build', 'run'), when='+colors')
