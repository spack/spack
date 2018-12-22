# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PySetuptoolsGit(PythonPackage):
    """Setuptools revision control system plugin for Git"""

    homepage = "https://pypi.python.org/pypi/setuptools-git"
    url      = "https://pypi.io/packages/source/s/setuptools-git/setuptools-git-1.2.tar.gz"

    version('1.2', '40b2ef7687a384ea144503c2e5bc67e2')

    depends_on('py-setuptools', type='build')
    depends_on('git')
