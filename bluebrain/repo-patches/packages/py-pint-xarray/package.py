# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPintXarray(PythonPackage):
    """Physical units interface to xarray using Pint."""

    homepage = "https://github.com/xarray-contrib/pint-xarray"
    pypi = "pint-xarray/pint-xarray-0.2.1.tar.gz"

    version('0.2.1', sha256='1ee6bf74ee7b52b946f226a96469276fa4f5c68f7381c1b2aae66852562cb275')

    depends_on('python@3.7:', type=('build', 'run'))

    depends_on('py-setuptools', type=('build', 'run'))

    depends_on('py-numpy@1.17:',        type=('build', 'run'))
    depends_on('py-pint@0.16:',         type=('build', 'run'))
    depends_on('py-xarray@0.16.1:',     type=('build', 'run'))
    depends_on('py-importlib-metadata', type=('build', 'run'), when='^python@:3.7')
