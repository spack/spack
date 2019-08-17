# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPycparser(PythonPackage):
    """A complete parser of the C language, written in pure python."""
    homepage = "https://github.com/eliben/pycparser"
    url      = "https://pypi.io/packages/source/p/pycparser/pycparser-2.17.tar.gz"

    import_modules = ['pycparser', 'pycparser.ply']

    version('2.18', '72370da54358202a60130e223d488136')
    version('2.17', 'ca98dcb50bc1276f230118f6af5a40c7')
    version('2.13', 'e4fe1a2d341b22e25da0d22f034ef32f')

    depends_on('py-setuptools', type='build')
