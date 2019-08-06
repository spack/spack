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

    # TODO add qt-designer as variant
    # TODO add python bindings as variant

    # QScintilla so far tested to compile with Qt@4.8.6
    depends_on('qt') #+phonon +dbus variants are causing compilation problems

    # Beyond py-pyqt@4.12.1, pyqt4 needs its own sip module (not implemented yet)
    # Without private sip moduele, python bindings will not compile
    # Ref: https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html   
    # TODO implement private sip module for py-pyqt4
    depends_on('py-pyqt4@:4.12.1', type='build', when='@qt4') 
    depends_on('py-pyqt5', type='build', when='qt@5')
    depends_on('python', type=('build', 'run'))

    # with qt@4.8.6, didn't have much luck in compiling newer versions
    conflicts('qt@4', when='@2.10.3:') 

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

    def make_designer_qt(self):
        pass # not implemented yet


    def make_variants(self):
        make_python_bindings(self)
        make_designer_qt(self)


    run_before('qmake')(chdir)

    run_after('install')(make_variants)
