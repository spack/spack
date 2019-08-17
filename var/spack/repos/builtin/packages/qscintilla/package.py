# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os

class Qscintilla(QMakePackage):
    """QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control. """

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.11.2/QScintilla_gpl-2.11.2.tar.gz"

    version('2.11.2', sha256='029bdc476a069fda2cea3cd937ba19cc7fa614fb90578caef98ed703b658f4a1')
    # didn't have much luck with newer versions of Qscintilla and QT@4.8.6, so prefer the following version
    version('2.10.2', sha256='14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0', preferred=True)

    variant('python', default=True, description="Enable python bindings")
    variant('designer', default=False, description="Enable pluging for Qt-Designer")

    # QScintilla so far tested to compile with Qt@4.8.6
    depends_on('qt') # qt is not compiling with +phonon +dbus variants enabled

    # Beyond py-pyqt@4.12.1, pyqt4 needs its own sip module (not implemented yet)
    # Without private sip moduele, python bindings will not compile
    # Ref: https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html···
    # TODO implement private sip module for py-pyqt4
    depends_on('py-pyqt4@:4.12.1', type='build')·
    #depends_on('py-pyqt5', type='build') # when='qt@5' not working?
    depends_on('python', type=('build', 'run'))
    depends_on('py-sip', type='build')

    # with qt@4.8.6, didn't have much luck in compiling newer versions
    conflicts('qt@4', when='@2.10.3:')·


    @run_before('qmake')
    def chdir(self):
        os.chdir(str(self.stage.source_path)+'/Qt4Qt5')


    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ['CONFIG+=-std=c++11', 'DEFINES+=NO_CXX11_REGEX=1']
        return args


    # currently installation is done under path "/qscintilla_prefix/qt_prefix"
    # without settting INSTALL_ROOT, qscintilla is installed under qt_prefix
    # giving 'Nothing Installed Error'
    def setup_environment(self, spack_env, run_env):
        spack_env.set('INSTALL_ROOT', self.prefix)


    @run_after('install')
    def make_variants(self):
        if '+python' in self.spec:
            os.chdir(str(self.stage.source_path)+'/Python')
            python = which('python')
            if self.spec['qt'].version < Version('5'):
                # headers are installed under qscintilla_prefix/qt_prefix/include
                full_prefix = str(self.prefix)+ str(self.spec['qt'].prefix)
                python('configure.py', '--qsci-incdir='+full_prefix+'/include')
            else:
                python('configure.py', '--pyqt=PyQt5')
        if '+designer' in self.spec:
            pass # not implemented yet TODO


    @run_after('qmake')
    def fix_install_path(self):
        makefile=FileFilter('Makefile')
        makefile.filter(r'\$\(INSTALL_ROOT\)'+self.spec['qt'].prefix, '$(INSTALL_ROOT)')
