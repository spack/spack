# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPythonLanguageServer(PythonPackage):
    """An implementation of the Language Server Protocol for Python"""

    homepage = "https://github.com/palantir/python-language-server"
    url      = "https://github.com/palantir/python-language-server/archive/0.15.1.tar.gz"

    version('0.15.1', 'deee6fe6776c4f59547939d356004650')

    depends_on('py-setuptools', type='build')
    depends_on('py-configparser', type=('build', 'run'))
    depends_on('py-future@0.14.0:', type=('build', 'run'))
    depends_on('py-futures', type=('build', 'run'))  # python_version == "2.7"',
    depends_on('py-jedi@0.10:', type=('build', 'run'))
    # FIXME:
    # 'json-rpc==1.10.8',
    depends_on('py-mccabe', type=('build', 'run'))
    depends_on('py-pycodestyle', type=('build', 'run'))
    # FIXME:
    # 'pydocstyle>=2.0.0',
    depends_on('py-pyflakes', type=('build', 'run'))
    depends_on('py-rope@0.10.5:', type=('build', 'run'))
    depends_on('py-yapf', type=('build', 'run'))
    depends_on('py-pluggy', type=('build', 'run'))
