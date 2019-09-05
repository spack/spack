# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPackaging(PythonPackage):
    """Core utilities for Python packages."""

    homepage = "https://github.com/pypa/packaging"
    url      = "https://pypi.io/packages/source/p/packaging/packaging-19.1.tar.gz"

    import_modules = ['packaging']

    version('19.1', sha256='c491ca87294da7cc01902edbe30a5bc6c4c28172b5138ab4e4aa1b9d7bfaeafe')
    version('17.1', '8baf8241d1b6b0a5fae9b00f359976a8')
    version('16.8', '53895cdca04ecff80b54128e475b5d3b')

    depends_on('python@2.7:2.8,3.4:', type=('build', 'run'))
    depends_on('py-attrs', type=('build', 'run'))
    depends_on('py-pyparsing@2.0.2:', type=('build', 'run'))
    depends_on('py-six', type=('build', 'run'))

    # Newer versions of setuptools require packaging. Although setuptools is an
    # optional dependency of packaging, if it is not found, setup.py will
    # fallback on distutils.core instead. Don't add a setuptools dependency
    # or we won't be able to bootstrap setuptools.

    # depends_on('py-setuptools', type='build')
