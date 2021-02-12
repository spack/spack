# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyQtpy(PythonPackage):
    """QtPy: Abtraction layer for PyQt5/PyQt4/PySide/PySide2"""

    homepage = "https://github.com/spyder-ide/qtpy"
    pypi = "QtPy/QtPy-1.2.1.tar.gz"

    version('1.9.0', sha256='2db72c44b55d0fe1407be8fba35c838ad0d6d3bb81f23007886dc1fc0f459c8d')
    version('1.8.0', sha256='eb66998a9049d276c75f26fc31554666504a7c1732cc3edd42a434c1fed01c92')
    version('1.7.1', sha256='e97275750934b3a1f4d8e263f5b889ae817ed36f26867ab0ce52be731ab1ed9e')
    version('1.2.1', sha256='5803ce31f50b24295e8e600b76cc91d7f2a3140a5a0d526d40226f9ec5e9097d')

    apis = ['pyqt5', 'pyqt4', 'pyside2', 'pyside']

    variant('api', default='pyqt5', description='Default QT API',
            values=apis, multi=False)

    depends_on('py-setuptools', type='build')
    for api in apis:
        depends_on('py-' + api, when='+' + api, type='run')

    def setup_run_environment(self, env):
        env.set('QT_API', self.spec.variants['api'].value)
