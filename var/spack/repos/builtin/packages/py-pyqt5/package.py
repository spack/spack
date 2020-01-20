# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class PyPyqt5(SIPPackage):
    """PyQt is a set of Python v2 and v3 bindings for The Qt Company's Qt
    application framework and runs on all platforms supported by Qt including
    Windows, OS X, Linux, iOS and Android. PyQt5 supports Qt v5."""

    homepage = "https://www.riverbankcomputing.com/software/pyqt/intro"
    url      = "https://www.riverbankcomputing.com/static/Downloads/PyQt5/5.13.0/PyQt5_gpl-5.13.0.tar.gz"
    list_url = "https://www.riverbankcomputing.com/software/pyqt/download5"

    sip_module = 'PyQt5.sip'
    import_modules = [
        'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtHelp',
        'PyQt5.QtMultimedia', 'PyQt5.QtMultimediaWidgets', 'PyQt5.QtNetwork',
        'PyQt5.QtOpenGL', 'PyQt5.QtPrintSupport', 'PyQt5.QtQml',
        'PyQt5.QtQuick', 'PyQt5.QtSvg', 'PyQt5.QtTest', 'PyQt5.QtWebChannel',
        'PyQt5.QtWebSockets', 'PyQt5.QtWidgets', 'PyQt5.QtXml',
        'PyQt5.QtXmlPatterns'
    ]

    version('5.13.0', sha256='0cdbffe5135926527b61cc3692dd301cd0328dd87eeaf1313e610787c46faff9')
    version('5.12.3', sha256='0db0fa37debab147450f9e052286f7a530404e2aaddc438e97a7dcdf56292110')

    variant('qsci', default=False, description='Build with QScintilla python bindings')

    # Without opengl support, I got the following error:
    # sip: QOpenGLFramebufferObject is undefined
    depends_on('qt@5:+opengl')
    depends_on('python@2.6:', type=('build', 'run'))
    depends_on('py-enum34', type=('build', 'run'), when='^python@:3.3')

    depends_on('qscintilla', when='+qsci')

    # For building Qscintilla python bindings
    resource(name='qscintilla',
             url='https://www.riverbankcomputing.com/static/Downloads/QScintilla/2.10.2/QScintilla_gpl-2.10.2.tar.gz',
             sha256='14b31d20717eed95ea9bea4cd16e5e1b72cee7ebac647cba878e0f6db6a65ed0',
             destination='spack-resource-qscintilla',
             when='^qscintilla@2.10.2'
    )

    # https://www.riverbankcomputing.com/static/Docs/PyQt5/installation.html
    def configure_args(self):
        args = [
            '--pyuic5-interpreter', self.spec['python'].command.path,
            '--sipdir', self.prefix.share.sip.PyQt5,
            '--stubsdir', join_path(site_packages_dir, 'PyQt5'),
        ]
        if '+qsci' in self.spec:
            args.extend(['--qsci-api-destdir', self.prefix.share.qsci])
        return args

    @run_after('install')
    def make_qsci(self):
        if '+qsci' in self.spec:
            rsrc_py_path = os.path.join(
                self.stage.source_path,
                'spack-resource-qscintilla/QScintilla_gpl-' +
                str(self.spec['qscintilla'].version), 'Python')
            with working_dir(rsrc_py_path):
                pydir = join_path(site_packages_dir, 'PyQt5')
                python = self.spec['python'].command
                python('configure.py', '--pyqt=PyQt5',
                       '--sip=' + self.prefix.bin.sip,
                       '--qsci-incdir=' +
                       self.spec['qscintilla'].prefix.include,
                       '--qsci-libdir=' + self.spec['qscintilla'].prefix.lib,
                       '--qsci-sipdir=' + self.prefix.share.sip.PyQt5,
                       '--apidir=' + self.prefix.share.qsci,
                       '--destdir=' + pydir,
                       '--pyqt-sipdir=' + self.prefix.share.sip.PyQt5,
                       '--sip-incdir=' + python_include_dir,
                       '--stubsdir=' + pydir)

                # Fix build errors
                # "QAbstractScrollArea: No such file or directory"
                # "qprinter.h: No such file or directory"
                # ".../Qsci.so: undefined symbol: _ZTI10Qsci...."
                qscipro = FileFilter('Qsci/Qsci.pro')
                link_qscilibs = 'LIBS += -L' + self.prefix.lib +\
                    ' -lqscintilla2_qt5'
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
