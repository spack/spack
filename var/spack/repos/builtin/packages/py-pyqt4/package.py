# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class PyPyqt4(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt4 supports Qt v4 and will build
    against Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.12.3/PyQt4_gpl_x11-4.12.3.tar.gz"

    sip_module = 'PyQt4.sip'
    import_modules = [
        'PyQt4', 'PyQt4.Qt', 'PyQt4.QtCore', 'PyQt4.QtDeclarative',
        'PyQt4.QtDesigner', 'PyQt4.QtGui', 'PyQt4.QtHelp',
        'PyQt4.QtMultimedia', 'PyQt4.QtNetwork', 'PyQt4.QtOpenGL',
        'PyQt4.QtScript', 'PyQt4.QtScriptTools', 'PyQt4.QtSql', 'PyQt4.QtSvg',
        'PyQt4.QtTest', 'PyQt4.QtWebKit', 'PyQt4.QtXml', 'PyQt4.QtXmlPatterns'
    ]

    version('4.12.3', sha256='a00f5abef240a7b5852b7924fa5fdf5174569525dc076cd368a566619e56d472')
    version('4.11.3', '997c3e443165a89a559e0d96b061bf70',
            url='http://sourceforge.net/projects/pyqt/files/PyQt4/PyQt-4.11.3/PyQt-x11-gpl-4.11.3.tar.gz')

    variant('qsci', default=False, description='Build with QScintilla python bindings')

    # Supposedly can also be built with Qt 5 compatibility layer
    depends_on('qt@:4')
    depends_on('qscintilla', when='+qsci')

    # https://www.riverbankcomputing.com/static/Docs/PyQt4/installation.html
    def configure_file(self):
        return 'configure-ng.py'

    def configure_args(self):
        return [
            '--pyuic4-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt4,
            '--stubsdir', join_path(site_packages_dir, 'PyQt4'),
            '--qsci-api-destdir', self.prefix.share+'/qsci'
        ]

    @run_after('install')
    def make_qsci(self):
        if '+qsci' in self.spec:
            with working_dir(str(self.spec['qscintilla'].prefix)+'/share/qscintilla/src/Python'):
                pydir = join_path(site_packages_dir, 'PyQt4')
                python = which('python')
                python('configure.py',
                       '--sip=' + self.prefix.bin + '/sip',
                       '--qsci-incdir=' + self.spec['qscintilla'].prefix.include,
                       '--qsci-libdir=' + self.spec['qscintilla'].prefix.lib,
                       '--qsci-sipdir=' + self.prefix.share.sip.PyQt4,
                       '--apidir=' + self.prefix + '/share/qsci',
                       '--destdir=' + pydir,
                       '--pyqt-sipdir=' + self.prefix.share.sip.PyQt4,
                       '--sip-incdir=' + self.prefix + '/include/python'+str(self.spec['python'].version.up_to(2)),
                       '--stubsdir='+pydir)

                # Fix build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                # ".../Qsci.so: undefined symbol: _ZTI10Qsci...."
                qscipro = FileFilter('Qsci/Qsci.pro')
                link_qscilibs = 'LIBS += -L'+self.prefix.lib+' -lqscintilla2_qt4'
                qscipro.filter('TEMPLATE = lib',
                               'TEMPLATE = lib\nQT += widgets\nQT += printsupport\n'+link_qscilibs)

                make()

                # Fix installation prefixes
                makefile = FileFilter('Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)','')
                makefile = FileFilter('Qsci/Makefile')
                makefile.filter(r'\$\(INSTALL_ROOT\)','')

                make('install')
