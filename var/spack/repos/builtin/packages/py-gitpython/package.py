# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitpython(PythonPackage):
    """
    GitPython is a python library used to interact with Git repositories.
    """

    homepage = "http://gitpython.readthedocs.org"
    url      = "https://pypi.io/packages/source/g/gitpython/GitPython-3.1.7.tar.gz"

    version('3.1.7', sha256='2db287d71a284e22e5c2846042d0602465c7434d910406990d5b74df4afb0858')

    depends_on('python@3.4:',   type=('build', 'run'))
    depends_on('py-setuptools', type='build')
    depends_on('py-gitdb@4.0.1:4.999', type=('build', 'run'))
