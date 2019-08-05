# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Qscintilla(QMakePackage):
    """FIXME: Put a proper description of your package here."""

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.11.2/QScintilla_gpl-2.11.2.tar.gz"

    version('2.11.2', sha256='029bdc476a069fda2cea3cd937ba19cc7fa614fb90578caef98ed703b658f4a1')
    # didn't have much luck with newer versions of Qscintilla and QT@4.8.6, so prefer the following version
    version('2.10.2', sha256='14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0', preferred=True)

    ## TODO build python pindings
    # TODO add qt-designer as variant
    depends_on('qt~phonon~dbus') #phonon and dbus are causing compilation problems
    depends_on('py-pyqt4', type='build') #when='qt@4' 
    depends_on('py-pyqt5', type='build', when='qt@5') #when='qt@4' 
    depends_on('python', type=('build', 'run'))

    conflicts('qt@4', when='@2.10.3:') # with qt@4.8.6, didn't have much luck with newer versions

    def chdir(self):
        os.chdir(str(self.stage.source_path)+'/Qt4Qt5')

    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ['CONFIG+=-std=c++11', 'DEFINES+=NO_CXX11_REGEX=1']
        return args

    # the following installs files under "/qscintilla_prefix/qmake_prefix"
    # it gets rid of 'Nothing installed error'
    # without it libqscintilla is installed under qt_prefix, is that how it should be?
    def setup_environment(self, spack_env, run_env):
        spack_env.set('INSTALL_ROOT', prefix)


    def make_python_bindings(self):
        os.chdir(str(self.stage.source_path)+'/Python')
        python = which('python')
        if self.version < Version('5'):
            python('configure.py')
        else:
            python('configure.py -pyqt=PyQt5')


    run_before('qmake')(chdir)

    run_after('install')(make_python_bindings)
