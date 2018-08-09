##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *
import glob


class Wireshark(CMakePackage):
    """Graphical network analyzer and capture tool"""

    homepage = "https://www.wireshark.org"
    url      = "https://www.wireshark.org/download/src/all-versions/wireshark-2.6.0.tar.xz"

    version('2.6.0', 'd9f9e206977da14427bfd66b582601ae')

    variant('smi',      default=False, description='Build with libsmi')
    variant('libssh',   default=False, description='Build with libssh')
    variant('nghttp2',  default=False, description='Build with nghttp2')
    variant('qt',       default=False, description='Build with qt')
    variant('gtk3',     default=False, description='Build with gtk3')
    variant('gtk',      default=False, description='Build with gtk')
    variant('headers',  default=True, description='Install headers')

    depends_on('bison',     type='build')
    depends_on('cares')
    depends_on('doxygen',   type='build')
    depends_on('flex',      type='build')
    depends_on('git',       type='build')
    depends_on('glib')
    depends_on('gnutls')
    depends_on('libgcrypt@1.4.2:')
    depends_on('libmaxminddb')
    depends_on('libtool@2.2.2:', type='build')
    depends_on('libpcap')
    depends_on('lua@5.0.0:5.2.99')
    depends_on('krb5')
    depends_on('pkgconfig', type='build')
    depends_on('libsmi',    when='+smi')
    depends_on('libssh',    when='+libssh')
    depends_on('nghttp2',   when='+nghttp2')
    depends_on('portaudio', when='+gtk')
    depends_on('portaudio', when='+gtk3')
    depends_on('qt@4.8:',   when='+qt')
    depends_on('gtkplus3',  when='+gtk3')
    depends_on('gtkplus',   when='+gtk')
    depends_on('adwaita-icon-theme', when='+gtk3')

    def cmake_args(self):
        args = ['-DENEABLE_CARES=ON',
                '-DENABLE_GNUTLS=ON',
                '-DENABLE_LUA=ON',
                '-DENABLE_MAXMINDDB=ON',
                '-DYACC_EXECUTABLE=' + self.spec['bison'].prefix.bin.yacc,
                '-DGIT_EXECUTABLE=' + self.spec['git'].prefix.bin.git,
                '-DPCAP_INCLUDE_DIR=' + self.spec['libpcap'].prefix.include,
                '-DPCAP_LIB=' + str(self.spec['libpcap'].libs),
                '-DLUA_INCLUDE_DIR=' + self.spec['lua'].prefix.include,
                '-DLUA_LIBRARY=' + str(self.spec['lua'].libs)
                ]
        if self.spec.satisfies('+qt'):
            args.append('-DBUILD_wireshark=ON')
            args.append('-DENABLE_APPLICATION_BUNDLE=ON')
            if self.spec['qt'].version >= Version(5):
                args.append('-DENABLE_QT5=ON')
            else:
                args.append('-DENABLE_QT5=OFF')
        else:
            args.append('-DBUILD_wireshark=OFF')
            args.append('-DENABLE_APPLICATION_BUNDLE=OFF')
            args.append('-DENABLE_QT5=OFF')

        if self.spec.satisfies('+gtk3') or self.spec.satisfies('+gtk'):
            args.append('-DBUILD_wireshark_gtk=ON')
            args.append('-DENABLE_PORTAUDIO=ON')
        else:
            args.append('-DBUILD_wireshark_gtk=OFF')
            args.append('-DENABLE_PORTAUDIO=OFF')
        if self.spec.satisfies('+gtk3'):
            args.append('-DENABLE_GTK3=ON')

        if self.spec.satisfies('+libssh'):
            args.append('-DBUILD_sshdump=ON')
            args.append('-DBUILD_ciscodump=ON')
        else:
            args.append('-DBUILD_sshdump=OFF')
            args.append('-DBUILD_ciscodump=OFF')

        if self.spec.satisfies('+smi'):
            args.append('-DBUILD_SMI=ON')
        else:
            args.append('-DBUILD_SMI=OFF')

        if self.spec.satisfies('+nghttp2'):
            args.append('-DBUILD_NGHTTP2=ON')
        else:
            args.append('-DBUILD_NGHTTP2=OFF')

        return args

    @run_after('install')
    def symlink(self):
        if self.spec.satisfies('platform=darwin'):
            link(join_path(self.prefix,
                           'Wireshark.app/Contents/MacOS/Wireshark'),
                 self.prefix.bin.wireshark)

    @run_after('install')
    def install_headers(self):
        if self.spec.satisfies('+headers'):
            folders = ['.', 'epan/crypt', 'epan/dfilter', 'epan/dissectors',
                       'epan/ftypes', 'epan/wmem', 'wiretap', 'wsutil']
            for folder in folders:
                headers = glob.glob(join_path(folder, '*.h'))
                for h in headers:
                    install(h, join_path(prefix.include, 'wireshark', folder))
