# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyVersioneer(PythonPackage):
    """Versioneer is a tool to automatically update version strings (in
    setup.py and the conventional 'from PROJECT import _version' pattern) by
    asking your version-control system about the current tree."""

    homepage = "https://github.com/warner/python-versioneer"
    url      = "https://github.com/warner/python-versioneer/archive/0.18.tar.gz"
    git      = "https://github.com/warner/python-versioneer.git"

    maintainers = ['scemama', 'warner']

    version('0.18', sha256='cf895b67f5bc62d61c4837458069ded8f66b4e5764c19f7253c51ee27e8b3a99')

    depends_on('python@2.7:')
#  depends_on('python@2.7:2.8.999', type=('build', 'run'), when='@0.10:1.999')
#  depends_on('python@3:', type=('build', 'run'), when='@0.18:')

    depends_on('py-setuptools', type='build')
