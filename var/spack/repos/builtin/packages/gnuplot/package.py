# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Gnuplot(AutotoolsPackage):
    """Gnuplot is a portable command-line driven graphing utility for Linux,
       OS/2, MS Windows, OSX, VMS, and many other platforms. The source
       code is copyrighted but freely distributed (i.e., you don't have
       to pay for it). It was originally created to allow scientists and
       students to visualize mathematical functions and data
       interactively, but has grown to support many non-interactive uses
       such as web scripting. It is also used as a plotting engine by
       third-party applications like Octave. Gnuplot has been supported
       and under active development since 1986

    """
    homepage = "http://www.gnuplot.info"
    url      = "http://downloads.sourceforge.net/project/gnuplot/gnuplot/5.0.6/gnuplot-5.0.6.tar.gz"

    # There is a conflict in term.h between gnuplot and ncurses, which is a
    # dependency of readline. Fix it with a small patch
    patch('term_include.patch')

    version('5.2.5', '039db2cce62ddcfd31a6696fe576f4224b3bc3f919e66191dfe2cdb058475caa')
    version('5.2.2', '60aedd08998160593199459dea8467fe')
    version('5.2.0', '0bd8f9af84c0ad2fa9de16772c366416')
    version('5.0.7', '8eaafddb0b12795f82ed6dd2a6ebbe80')
    version('5.0.6', '8ec46520a86a61163a701b00404faf1a')
    version('5.0.5', 'c5e96fca73afbee4f57cbc1bfce6b3b8')
    version('5.0.1', '79b4f9e203728f76b60b28bcd402d3c7')

    variant('wx',      default=False,
            description='Activates wxWidgets terminal')
    variant('gd',      default=True,
            description='Activates gd based terminal')
    variant('cairo',   default=True,
            description='Activates cairo based terminal')
    variant('X',       default=False,
            description='Build with X11')
    variant('libcerf', default=True,
            description='Build with libcerf support')
    variant('pbm',     default=False,
            description='Enable PBM (Portable Bit Map) and other older bitmap terminals')  # NOQA: ignore=E501
    variant('qt',      default=False,
            description='Build with QT')

    # required dependencies
    depends_on('readline')
    depends_on('pkgconfig', type='build')
    depends_on('libxpm')
    depends_on('libiconv')

    # optional dependencies:
    depends_on('libcerf', when='+libcerf')
    depends_on('libgd', when='+gd')
    depends_on('cairo@1.2:', when='+cairo')
    depends_on('wxwidgets', when='+wx')
    depends_on('pango@1.10:', when='+wx')
    depends_on('pango@1.10:', when='+cairo')
    depends_on('libx11', when='+X')
    depends_on('qt@5.7:+opengl', when='+qt')

    def configure_args(self):
        # see https://github.com/Homebrew/homebrew-core/blob/master/Formula/gnuplot.rb
        # and https://github.com/macports/macports-ports/blob/master/math/gnuplot/Portfile
        spec = self.spec
        options = [
            '--disable-dependency-tracking',
            '--disable-silent-rules',
            # Per upstream: "--with-tutorial is horribly out of date."
            '--without-tutorial',
            '--with-readline=%s' % spec['readline'].prefix
        ]

        if '+pbm' in spec:
            options.append('--with-bitmap-terminals')
        else:
            options.append('--without-bitmap-terminals')

        if '+X' in spec:
            # It seems there's an open bug for wxWidgets support
            # See : http://sourceforge.net/p/gnuplot/bugs/1694/
            os.environ['TERMLIBS'] = '-lX11'
            options.append('--with-x')
        else:
            options.append('--without-x')

        if '+qt' in spec:
            options.append('--with-qt=qt5')
            # QT needs C++11 compiler:
            os.environ['CXXFLAGS'] = '{0}'.format(self.compiler.cxx11_flag)

            if spec.satisfies('platform=darwin'):
                qt_path = spec['qt'].prefix
                # see
                # http://gnuplot.10905.n7.nabble.com/Building-with-Qt-depends-on-pkg-config-Qt-5-term-doesn-t-work-on-OS-X-td18063.html
                os.environ['QT_LIBS'] = (
                    '-F{0}/lib ' +
                    '-framework QtCore ' +
                    '-framework QtGui ' +
                    '-framework QtWidgets ' +
                    '-framework QtNetwork ' +
                    '-framework QtSvg ' +
                    '-framework QtPrintSupport').format(qt_path)

                os.environ['QT_CFLAGS'] = (
                    '-F{0}/lib ' +
                    '-I{0}/lib/QtCore.framework/Headers ' +
                    '-I{0}/lib/QtGui.framework/Headers ' +
                    '-I{0}/lib/QtWidgets.framework/Headers ' +
                    '-I{0}/lib/QtNetwork.framework/Headers ' +
                    '-I{0}/lib/QtSvg.framework/Headers').format(qt_path)
        else:
            options.append('--with-qt=no')

        if '+wx' in spec:
            options.append('--with-wx=%s' % spec['wx'].prefix)
        else:
            options.append('--disable-wxwidgets')

        if '+gd' in spec:
            options.append('--with-gd=%s' % spec['libgd'].prefix)
        else:
            options.append('--without-gd')

        if '+cairo' in spec:
            options.append('--with-cairo')
        else:
            options.append('--without-cairo')

        if '+libcerf' in spec:
            options.append('--with-libcerf')
        else:
            options.append('--without-libcerf')

        # TODO: Enable pdflib-based pdf terminal
        # '--with-pdf=%s' % spec['pdflib-lite'].prefix  (or pdflib)
        options.append('--without-pdf')

        # TODO: Enable lua-based terminals
        options.append('--without-lua')

        # TODO: --with-latex
        options.append('--without-latex')

        # TODO: --with-aquaterm  depends_on('aquaterm')
        options.append('--without-aquaterm')

        return options
