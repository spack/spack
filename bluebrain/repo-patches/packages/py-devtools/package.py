# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyDevtools(PythonPackage):
    """Dev tools for python.
    The debug print command python never had (and other things)."""

    homepage = "https://python-devtools.helpmanual.io/"
    url      = "https://pypi.io/packages/source/d/devtools/devtools-0.5.1.tar.gz"

    version('0.5.1', sha256='51ca8d2e15b8a862875a4837db2bafbc6cda409c069e960aec3f4bbd91fe9c08')

    variant('pygments', default=False, description='PyPygments dependency')

    depends_on('python@3.5:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'), when='+pygments')
