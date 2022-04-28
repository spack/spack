# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPydocstyle(PythonPackage):
    """Python docstring style checker."""

    homepage = "https://github.com/PyCQA/pydocstyle/"
    pypi     = "pydocstyle/pydocstyle-6.1.1.tar.gz"

    version('6.1.1', sha256='1d41b7c459ba0ee6c345f2eb9ae827cab14a7533a88c5c6f7e94923f72df92dc')

    variant('toml', default=True, description='Allow pydocstyle to read pyproject.toml')

    depends_on('python@3.6:', type=('build', 'run'))
    depends_on('py-setuptools', type=('build', 'run'))
    depends_on('py-snowballstemmer', type=('build', 'run'))
    depends_on('py-toml', when='+toml', type=('build', 'run'))
