# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtpy(PythonPackage):
    """QtPy: Abtraction layer for PyQt5/PyQt4/PySide"""

    homepage = "https://github.com/spyder-ide/qtpy"
    url      = "https://pypi.io/packages/source/Q/QtPy/QtPy-1.2.1.tar.gz"

    version('1.2.1', sha256='5803ce31f50b24295e8e600b76cc91d7f2a3140a5a0d526d40226f9ec5e9097d')

    depends_on('py-setuptools', type='build')
    depends_on('py-pyqt4',    type=('build', 'run'))
