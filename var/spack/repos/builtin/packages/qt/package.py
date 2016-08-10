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
    url      = 'http://download.qt.io/archive/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz'
    list_url = 'http://download.qt.io/archive/qt/'
    list_depth = 4

    version('5.7.0',  '9a46cce61fc64c20c3ac0a0e0fa41b42')
    version('5.5.1',  '59f0216819152b77536cf660b015d784')
    version('5.4.2',  'fa1c4d819b401b267eb246a543a63ea5')
    version('5.4.0',  'e8654e4b37dd98039ba20da7a53877e6')
    version('5.3.2',  'febb001129927a70174467ecb508a682')
    version('5.2.1',  'a78408c887c04c34ce615da690e0b4c8')
    version('4.8.6',  '2edbe4d6c2eff33ef91732602f3518eb')
    version('3.3.8b', '9f05b4125cfe477cc52c9742c3c09009')

    # Add patch for compile issues with qt3 found with use in the
    # OpenSpeedShop project
    variant('krellpatch', default=False, description="Build with openspeedshop based patch.")
    variant('mesa',       default=False, description="Depend on mesa.")
    variant('gtk',        default=False, description="Build with gtkplus.")

    patch('qt3krell.patch', when='@3.3.8b+krellpatch')

    # https://github.com/xboxdrv/xboxdrv/issues/188
    patch('btn_trigger_happy.patch', when='@5.7.0:')

    # Use system openssl for security.
    # depends_on("openssl")

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
    # depends_on("flex", type='build')
    # depends_on("bison", type='build')
    # depends_on("ruby")
    # depends_on("icu4c")

    # OpenGL hardware acceleration
    depends_on("mesa", when='@4:+mesa')
    depends_on("libxcb")

    def url_for_version(self, version):
        # URL keeps getting more complicated with every release
        url = self.list_url

        if version >= Version('4.0'):
            url += version.up_to(2) + '/'
        else:
            url += version.up_to(1) + '/'

        if version >= Version('4.8'):
            url += str(version) + '/'

        if version >= Version('5'):
            url += 'single/'

        url += 'qt-'

        if version >= Version('4.6'):
            url += 'everywhere-'
        elif version >= Version('2.1'):
            url += 'x11-'

        if version >= Version('4.0'):
            url += 'opensource-src-'
        elif version >= Version('3'):
            url += 'free-'

        url += str(version) + '.tar.gz'

        return url

    def setup_environment(self, spack_env, env):
        env.set('QTDIR', self.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dspec):
        spack_env.set('QTDIR', self.prefix)

    def patch(self):
        if self.spec.satisfies('@4'):
            # Fix qmake compilers in the default mkspec
            filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc',
                        'mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++',
                        'mkspecs/common/g++-base.conf')

            # Necessary to build with GCC 6 and other modern compilers
            # http://stackoverflow.com/questions/10354371/
            filter_file('(^QMAKE_CXXFLAGS .*)', r'\1 -std=gnu++98',
                        'mkspecs/common/gcc-base.conf')

            filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                        'mkspecs/common/g++-unix.conf')
        elif self.spec.satisfies('@5:'):
            # Fix qmake compilers in the default mkspec
            filter_file('^QMAKE_COMPILER .*', 'QMAKE_COMPILER = cc',
                        'qtbase/mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc',
                        'qtbase/mkspecs/common/g++-base.conf')
            filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++',
                        'qtbase/mkspecs/common/g++-base.conf')

            filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                        'qtbase/mkspecs/common/g++-unix.conf')

    @property
    def common_config_args(self):
        return [
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

    # Don't disable all the database drivers, but should
    # really get them into spack at some point.

    @when('@3')
    def configure(self):
        # A user reported that this was necessary to link Qt3 on ubuntu
        os.environ['LD_LIBRARY_PATH'] = os.getcwd() + '/lib'
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
                  '{0}-gtkstyle'.format('' if '+gtk' in self.spec else '-no'),
                  *self.common_config_args)

    @when('@5.0:5.6')
    def configure(self):
        configure('-no-eglfs',
                  '-no-directfb',
                  '-qt-xcb',
                  '{0}-gtkstyle'.format('' if '+gtk' in self.spec else '-no'),
                  '-skip', 'qtwebkit',
                  *self.common_config_args)

    @when('@5.7:')
    def configure(self):
        configure('-no-eglfs',
                  '-no-directfb',
                  '-qt-xcb',
                  '{0}-gtk'.format('' if '+gtk' in self.spec else '-no'),
                  *self.common_config_args)

    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")
