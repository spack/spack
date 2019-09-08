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

    variant('python', default=False, description="Enable python bindings")
    variant('designer', default=False, description="Enable pluging for Qt-Designer")

    depends_on('qt') # qt@4 is not compiling with +phonon +dbus variants enabled


    # Beyond py-pyqt@4.12.1, pyqt needs its own sip module (not implemented yet)
    # Without private sip module, python bindings will not compile
    # Ref: https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html
    # TODO implement private sip module for py-pyqt4
    depends_on('py-pyqt4', type=('build', 'run'), when='^qt@4 +python')
    depends_on('py-pyqt5', type=('build', 'run'), when='^qt@5 +python')
    depends_on('python', type=('build', 'run'), when='+python')

    # with qt@4.8.6, didn't have much luck in compiling newer versions
    conflicts('qt@4', when='@2.10.3:')
    # conflicts('py-pyqt4@4.12.2:', when='+python') # private sip module not implemented yet
    # conflicts('py-pyqt5', when='+python') # private sip module not implemented yet

    @run_before('qmake')
    def chdir(self):
        os.chdir(str(self.stage.source_path)+'/Qt4Qt5')


    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ['CONFIG+=-std=c++11', 'DEFINES+=NO_CXX11_REGEX=1']
        return args


    # When INSTALL_ROOT is unset, qscintilla is installed under qt_prefix
    # giving 'Nothing Installed Error'
    def setup_environment(self, spack_env, run_env):
        spack_env.set('INSTALL_ROOT', self.prefix)


    @run_after('install')
    def make_variants(self):
        if '+python' in self.spec:
            os.chdir(str(self.stage.source_path)+'/Python')
            python = which('python')
            if 'py-pyqt4' in self.spec:
                pydir = self.prefix.lib+'python'+str(self.spec['python'].version)+'/site-packages/PyQt4'
                pyqtsipdir = '--pyqt-sipdir='+self.spec['py-pyqt5'].prefix+'/share/sip/PyQt4'
            elif 'py-pyqt5' in self.spec:
                pydir = self.prefix.lib+'python'+str(self.spec['python'].version)+'/site-packages/PyQt5'
                pyqtsipdir = '--pyqt-sipdir='+self.spec['py-pyqt5'].prefix+'/share/sip/PyQt5'

            carg_inc = '--qsci-incdir='+self.prefix.include
            carg_lib = '--qsci-libdir='+self.prefix.lib
            mkdirp(self.prefix+'/share/sip')
            carg_sip = '--qsci-sipdir='+self.prefix+'/share/sip'
            carg_api = '--apidir='+self.prefix+'/qsci'
            carg_dest = '--destdir='+pydir
            carg_sipinc = '--sip-incdir='+self.spec['py-sip'].prefix+'/include'

            if self.spec['qt'].version < Version('5'):
                python('configure.py', carg_inc, carg_lib, carg_sip, carg_api, carg_dest, pyqtsipdir, carg_sipinc)
            else:
                python('configure.py', '--pyqt=PyQt5', carg_inc, carg_lib, carg_sip, carg_api, carg_dest, pyqtsipdir, carg_sipinc)
        if '+designer' in self.spec:
            pass # not implemented yet TODO


    @run_after('qmake')
    def fix_install_path(self):
        makefile = FileFilter('Makefile')
        makefile.filter(r'\$\(INSTALL_ROOT\)' + self.spec['qt'].prefix, '$(INSTALL_ROOT)')
