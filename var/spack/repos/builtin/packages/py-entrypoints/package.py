# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyEntrypoints(PythonPackage):
    """Discover and load entry points from installed packages."""

    homepage = "https://pypi.python.org/pypi/entrypoints"
    url      = "https://pypi.io/packages/source/e/entrypoints/entrypoints-0.2.3.tar.gz"

    import_modules = ['entrypoints']

    version('0.2.3', '0d3ad1b0130d91e3596ef3a59f25a56c')

    depends_on('python@2.7:', type=('build', 'run'))
    depends_on('py-configparser', when='^python@:2.8', type=('build', 'run'))
