# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.pkg.builtin.py_prettytable import PyPrettytable as BuiltinPyPrettytable


class PyPrettytable(BuiltinPyPrettytable):
    __doc__ = BuiltinPyPrettytable.__doc__

    version('2.2.1', sha256='6d465005573a5c058d4ca343449a5b28c21252b86afcdfa168cdc6a440f0b24c')

    depends_on('python@3.6:', when='@2.0.0:', type=('build', 'run'))
    depends_on('py-setuptools-scm', type='build')
    depends_on('py-importlib-metadata', when='@2.2.1:^python@:3.8', type=('build', 'run'))
    depends_on('py-wcwidth', when='@1.0.0:', type=('build', 'run'))
