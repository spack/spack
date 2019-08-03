# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: MIT
#
# ----------------------------------------------------------------------------
#
#     spack install py-gitpython
#
# You can edit this file again by typing:
#
#     spack edit py-gitpython
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *

class PyGitpython(PythonPackage):
    """GitPython is a python library used to interact with Git repositories."""

    homepage = "http://gitpython.readthedocs.org"
    url      = "https://github.com/gitpython-developers/GitPython/archive/2.1.13.tar.gz"

    version('2.1.13', sha256='ebbb2ea6064f97353cb711844e2e03b7df18fe6e47b70b1833e59b7bdacc9cc5')

    depends_on('py-setuptools', type='build')
    depends_on('py-gitdb',      type=('build', 'run'))

