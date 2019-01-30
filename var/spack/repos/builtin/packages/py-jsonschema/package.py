# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyJsonschema(PythonPackage):
    """Jsonschema: An(other) implementation of JSON Schema for Python."""

    homepage = "http://github.com/Julian/jsonschema"
    url      = "https://pypi.io/packages/source/j/jsonschema/jsonschema-2.5.1.tar.gz"

    version('2.5.1', '374e848fdb69a3ce8b7e778b47c30640')

    depends_on('py-setuptools', type='build')
    depends_on('py-vcversioner', type=('build', 'run'))

    # This dependency breaks concretization
    # See https://github.com/spack/spack/issues/2793
    # depends_on('py-functools32', when="^python@2.7", type=('build', 'run'))
    depends_on('py-functools32', type=('build', 'run'))
