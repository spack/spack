# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtawesome(PythonPackage):
    """FontAwesome icons in PyQt and PySide applications"""

    homepage = "https://github.com/spyder-ide/qtawesome"
    url = "https://pypi.io/packages/source/Q/QtAwesome/QtAwesome-0.4.1.tar.gz"

    version('0.4.1', 'bf93df612a31f3b501d751fc994c1b05')
    version('0.3.3', '830677aa6ca4e7014e228147475183d3')

    depends_on('py-setuptools', type='build')
    depends_on('py-qtpy',       type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
