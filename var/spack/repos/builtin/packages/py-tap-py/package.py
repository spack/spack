# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTapPy(PythonPackage):
    """Python TAP interface module for unit tests"""

    homepage = "https://github.com/mblayman/tappy"
    url      = "https://pypi.io/packages/source/t/tap.py/tap.py-1.6.tar.gz"

    version('1.6', sha256='3ee315567cd1cf444501c405b7f7146ffdb2e630bac58d0840d378a3b9a0dbe4')

    extends('python', ignore='bin/nosetests|bin/pygmentize')

    depends_on('python@2.6:2.8,3.2:3.4')
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
