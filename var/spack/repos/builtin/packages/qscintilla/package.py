# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qscintilla(QMakePackage):
    """
    QScintilla is a port to Qt of Neil Hodgson's Scintilla C++ editor control.
    """

    homepage = "https://www.riverbankcomputing.com/software/qscintilla/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.11.2/QScintilla_gpl-2.11.2.tar.gz"

    version('2.11.2', sha256='029bdc476a069fda2cea3cd937ba19cc7fa614fb90578caef98ed703b658f4a1')
    # Newer versions of Qscintilla won't build, so prefer the following version
    version('2.10.2', sha256='14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0', preferred=True)

    variant('designer', default=False, description="Enable pluging for Qt-Designer")
    variant('python', default=False, description="Build python bindings")

    depends_on('qt')
    depends_on('py-pyqt5 +qsci_api', type=('build', 'run'),  when='+python ^qt@5')
    depends_on('py-pyqt4 +qsci_api', type=('build', 'run'),  when='+python ^qt@4')
    depends_on('python',   type=('build', 'run'),  when='+python')

    extends('python', when='+python')

    @run_before('qmake')
    def chdir(self):
        os.chdir(str(self.stage.source_path) + '/Qt4Qt5')

    def qmake_args(self):
        # below, DEFINES ... gets rid of ...regex...errors during build
        # although, there shouldn't be such errors since we use '-std=c++11'
        args = ['CONFIG+=-std=c++11', 'DEFINES+=NO_CXX11_REGEX=1']
        return args

    # When INSTALL_ROOT is unset, qscintilla is installed under qt_prefix
    # giving 'Nothing Installed Error'
    def setup_build_environment(self, env):
        env.set('INSTALL_ROOT', self.prefix)

    def setup_run_environment(self, env):
        env.prepend_path('QT_PLUGIN_PATH', self.prefix.plugins)

    # Fix install prefix
    @run_after('qmake')
    def fix_install_path(self):
        makefile = FileFilter('Makefile')
        makefile.filter(r'\$\(INSTALL_ROOT\)' +
                        self.spec['qt'].prefix, '$(INSTALL_ROOT)')

    @run_after('install')
    def postinstall(self):
        # Make designer plugin
        if '+designer' in self.spec:
            with working_dir(os.path.join(self.stage.source_path,
                             'designer-Qt4Qt5')):
                qscipro = FileFilter('designer.pro')
                qscipro.filter('TEMPLATE = lib',
                               'TEMPLATE = lib\nINCLUDEPATH += ../Qt4Qt5\n')

                qmake()
                make()
                makefile = FileFilter('Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)' +
                                self.spec['qt'].prefix, '$(INSTALL_ROOT)')
                make('install')

    @run_after('install')
    def make_qsci(self):
        if '+python' in self.spec:
            if '^py-pyqt4' in self.spec:
                py_pyqtx = 'py-pyqt4'
                PyQtX = 'PyQt4'
            elif '^py-pyqt5' in self.spec:
                py_pyqtx = 'py-pyqt5'
                PyQtX = 'PyQt5'

            with working_dir(self.stage.source_path + '/Python'):
                pydir = join_path(
                    self.prefix,
                    self.spec['python'].package.site_packages_dir,
                    PyQtX)
                mkdirp(os.path.join(self.prefix.share.sip, PyQtX))
                python = self.spec['python'].command
                python('configure.py', '--pyqt=' + PyQtX,
                       '--sip=' + self.spec['py-sip'].prefix.bin.sip,
                       '--qsci-incdir=' + self.spec.prefix.include,
                       '--qsci-libdir=' + self.spec.prefix.lib,
                       '--qsci-sipdir=' +
                       os.path.join(self.prefix.share.sip, PyQtX),
                       '--apidir=' + self.prefix.share.qsci,
                       '--destdir=' + pydir,
                       '--pyqt-sipdir=' + os.path.join(
                           self.spec[py_pyqtx].prefix.share.sip, PyQtX),
                       '--sip-incdir=' +
                       join_path(self.spec['py-sip'].prefix.include,
                                 'python' +
                                 str(self.spec['python'].version.up_to(2))),
                       '--stubsdir=' + pydir)

                # Fix build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                # ".../Qsci.so: undefined symbol: _ZTI10Qsci...."
                qscipro = FileFilter('Qsci/Qsci.pro')
                if '^qt@4' in self.spec:
                    qtX = 'qt4'
                elif '^qt@5' in self.spec:
                    qtX = 'qt5'

                link_qscilibs = 'LIBS += -L' + self.prefix.lib +\
                    ' -lqscintilla2_' + qtX
                qscipro.filter('TEMPLATE = lib',
                               'TEMPLATE = lib\nQT += widgets' +
                               '\nQT += printsupport\n' + link_qscilibs)

                make()

                # Fix installation prefixes
                makefile = FileFilter('Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)', '')
                makefile = FileFilter('Qsci/Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)', '')

                make('install')

    @run_after('install')
    def extend_path_setup(self):
        # See github issue #14121 and PR #15297
        module = self.spec['py-sip'].variants['module'].value
        if module != 'sip':
            module = module.split('.')[0]
            with working_dir(site_packages_dir):
                with open(os.path.join(module, '__init__.py'), 'w') as f:
                    f.write('from pkgutil import extend_path\n')
                    f.write('__path__ = extend_path(__path__, __name__)\n')
