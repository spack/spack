# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtpy(PythonPackage):
    """QtPy: Abtraction layer for PyQt5/PyQt4/PySide/PySide2"""

    homepage = "https://github.com/spyder-ide/qtpy"
    url      = "https://pypi.io/packages/source/Q/QtPy/QtPy-1.2.1.tar.gz"

    version('1.2.1', sha256='5803ce31f50b24295e8e600b76cc91d7f2a3140a5a0d526d40226f9ec5e9097d')
    version('1.7.1', sha256='e97275750934b3a1f4d8e263f5b889ae817ed36f26867ab0ce52be731ab1ed9e')

    variant('qt4', default=False, description="Enable qt4 support")
    variant('qt5', default=True, description="Enable qt5 support")
    variant('pyside2', default=False, description="Enable pyside2 support")
    variant('pyside', default=False, description="Enable pyside support")

    depends_on('py-setuptools', type='build')
    depends_on('py-pyqt4',    type=('build', 'run'), when="+qt4")
    depends_on('py-pyqt5',    type=('build', 'run'), when="+qt5")
    depends_on('py-pyside',   type=('build', 'run'), when="+pyside")
    depends_on('py-pyside2',  type=('build', 'run'), when="+pyside2")
