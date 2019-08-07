# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtpy(PythonPackage):
    """QtPy: Abtraction layer for PyQt5/PyQt4/PySide"""

    homepage = "https://github.com/spyder-ide/qtpy"
    url      = "https://pypi.io/packages/source/Q/QtPy/QtPy-1.2.1.tar.gz"

    version('1.2.1', 'e2f783fb7f8e502815237bd8d30c6d11')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyqt4',    type=('build', 'run'))
