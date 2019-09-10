# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyGitdb2(PythonPackage):
    """GitDB is a pure-Python git object database
    """

    homepage = "https://github.com/gitpython-developers/gitdb"
    url      = "https://pypi.io/packages/source/g/gitdb2/gitdb2-3.11.2.tar.gz"

    version('2.0.5', '83361131a1836661a155172932a13c08bda2db3674e4caa32368aa6eb02f38c2')

    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-smmap2', type='run')
