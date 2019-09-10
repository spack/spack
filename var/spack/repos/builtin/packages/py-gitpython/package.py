# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories
    """

    homepage = "https://github.com/gitpython-developers/GitPython"
    url      = "https://pypi.io/packages/source/G/GitPython/GitPython-3.11.2.tar.gz"

    version('3.0.2', 'd2f4945f8260f6981d724f5957bc076398ada55cb5d25aaee10108bcdc894100')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-gitdb2', type='run')
