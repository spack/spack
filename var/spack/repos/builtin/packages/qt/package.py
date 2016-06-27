##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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
import os

class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'

    version('5.5.1',  '59f0216819152b77536cf660b015d784')
    version('5.4.2',  'fa1c4d819b401b267eb246a543a63ea5')
    version('5.4.0',  'e8654e4b37dd98039ba20da7a53877e6')
    version('5.3.2',  'febb001129927a70174467ecb508a682')
    version('5.2.1',  'a78408c887c04c34ce615da690e0b4c8')
    version('4.8.6',  '2edbe4d6c2eff33ef91732602f3518eb')
    version('3.3.8b', '9f05b4125cfe477cc52c9742c3c09009')

    # Add patch for compile issues with qt3 found with use in the OpenSpeedShop project
    variant('krellpatch', default=False, description="Build with openspeedshop based patch.")
    variant('mesa',       default=False, description="Depend on mesa.")
    variant('gtk',        default=False, description="Build with gtkplus.")

    patch('qt3krell.patch', when='@3.3.8b+krellpatch')

    # Use system openssl for security.
    #depends_on("openssl")

    depends_on("glib")
    depends_on("gtkplus", when='+gtk')
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("dbus", when='@4:')
    depends_on("libtiff")
    depends_on("libpng@1.2.56", when='@3')
    depends_on("libpng", when='@4:')
    depends_on("libmng")
    depends_on("jpeg")

    # Webkit
    # depends_on("gperf")
    # depends_on("flex")
    # depends_on("bison")
    # depends_on("ruby")
    # depends_on("icu4c")

    # OpenGL hardware acceleration
    depends_on("mesa", when='@4:+mesa')
    depends_on("libxcb")


    def url_for_version(self, version):
        url = "http://download.qt.io/archive/qt/"

        if version >= Version('5'):
            url += "%s/%s/single/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version, version)
        elif version >= Version('4.8'):
            url += "%s/%s/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version, version)
        elif version >= Version('4.6'):
            url += "%s/qt-everywhere-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version)
        elif version >= Version('4.0'):
            url += "%s/qt-x11-opensource-src-%s.tar.gz" % \
                    (version.up_to(2), version)
        elif version >= Version('3'):
            url += "%s/qt-x11-free-%s.tar.gz" % \
                    (version.up_to(1), version)
        elif version >= Version('2.1'):
            url += "%s/qt-x11-%s.tar.gz" % \
                    (version.up_to(1), version)
        else:
            url += "%s/qt-%s.tar.gz" % \
                    (version.up_to(1), version)

        return url


    def setup_environment(self, spack_env, env):
        env.set('QTDIR', self.prefix)


    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('QTDIR', self.prefix)


    def patch(self):
        if self.spec.satisfies('@4'):
            qmake_conf      = 'mkspecs/common/g++-base.conf'
            qmake_unix_conf = 'mkspecs/common/g++-unix.conf'
        elif self.spec.satisfies('@5'):
            qmake_conf      = 'qtbase/mkspecs/common/g++-base.conf'
            qmake_unix_conf = 'qtbase/mkspecs/common/g++-unix.conf'
        else:
            return

        # Fix qmake compilers in the default mkspec
        filter_file(r'^QMAKE_COMPILER *=.*$',  'QMAKE_COMPILER = cc', qmake_conf)
        filter_file(r'^QMAKE_CC *=.*$',        'QMAKE_CC = cc',       qmake_conf)
        filter_file(r'^QMAKE_CXX *=.*$',       'QMAKE_CXX = c++',     qmake_conf)
        filter_file(r'^QMAKE_LFLAGS_NOUNDEF *\+?=.*$',  'QMAKE_LFLAGS_NOUNDEF =', qmake_unix_conf)


    @property
    def common_config_args(self):
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-opengl',
            '-release',
            '-shared',
            '-confirm-license',
            '-openssl-linked',
            '-dbus-linked',
            '-optimized-qmake',
            '-no-openvg',
            '-no-pch',
            # NIS is deprecated in more recent glibc
            '-no-nis'
        ]

        if '+gtk' in self.spec:
            config_args.append('-gtkstyle')
        else:
            config_args.append('-no-gtkstyle')

        return config_args

    # Don't disable all the database drivers, but should
    # really get them into spack at some point.

    @when('@3')
    def configure(self):
        # An user report that this was necessary to link Qt3 on ubuntu
        os.environ['LD_LIBRARY_PATH'] = os.getcwd()+'/lib' 
        configure('-prefix', self.prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast')

    @when('@4')
    def configure(self):
        configure('-fast',
                  '-no-webkit',
                  *self.common_config_args)


    @when('@5')
    def configure(self):
        configure('-no-eglfs',
                  '-no-directfb',
                  '-qt-xcb',
                  # If someone wants to get a webkit build working, be my guest!
                  '-skip', 'qtwebkit',
                  *self.common_config_args)


    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")
