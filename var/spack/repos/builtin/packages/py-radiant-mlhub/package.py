# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class PyRadiantMlhub(PythonPackage):
    """A Python client for Radiant MLHub."""

    homepage = "https://github.com/radiantearth/radiant-mlhub"
    pypi     = "radiant-mlhub/radiant_mlhub-0.2.1.tar.gz"

    maintainers = ['adamjstewart']

    version('0.2.1', sha256='75a2f096b09a87191238fe557dc64dda8c44156351b4026c784c848c7d84b6fb')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-requests@2.25.1:2.25', type=('build', 'run'))
    depends_on('py-pystac@0.5.4', type=('build', 'run'))
    depends_on('py-click@7.1.2:7.1', type=('build', 'run'))
    depends_on('py-tqdm@4.56.0:4.56', type=('build', 'run'))
