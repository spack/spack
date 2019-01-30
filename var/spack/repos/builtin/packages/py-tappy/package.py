# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyTappy(PythonPackage):
    """Python TAP interface module for unit tests"""
    homepage = "https://github.com/mblayman/tappy"
    # base https://pypi.python.org/pypi/cffi
    url      = "https://pypi.io/packages/source/t/tap.py/tap.py-1.6.tar.gz"

    version('1.6', 'c8bdb93ad66e05f939905172a301bedf')

    extends('python', ignore='bin/nosetests|bin/pygmentize')

    depends_on('python@2.6:2.8,3.2:3.4')
    depends_on('py-nose', type=('build', 'run'))
    depends_on('py-pygments', type=('build', 'run'))
    depends_on('py-setuptools', type='build')
