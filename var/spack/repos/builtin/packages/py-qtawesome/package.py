# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtawesome(PythonPackage):
    """FontAwesome icons in PyQt and PySide applications"""

    homepage = "https://github.com/spyder-ide/qtawesome"
    url = "https://pypi.io/packages/source/Q/QtAwesome/QtAwesome-0.4.1.tar.gz"

    version('0.4.1', 'd55472b231eba07059794769bdfe07b2')
    version('0.3.3', '830677aa6ca4e7014e228147475183d3')

    depends_on('py-setuptools', type='build')
    depends_on('py-qtpy',       type=('build', 'run'))
    depends_on('py-six',        type=('build', 'run'))
