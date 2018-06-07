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
import platform
import os
import sys


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'
    # Alternative location 'http://download.qt.io/official_releases/qt/'
    url      = 'http://download.qt.io/archive/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz'
    list_url = 'http://download.qt.io/archive/qt/'
    list_depth = 3

    version('5.10.0', 'c5e275ab0ed7ee61d0f4b82cd471770d')
    version('5.9.1',  '77b4af61c49a09833d4df824c806acaf')
    version('5.9.0',  '9c8bc8b828c2b56721980368266df9d9')
    version('5.8.0',  'a9f2494f75f966e2f22358ec367d8f41')
    version('5.7.1',  '031fb3fd0c3cc0f1082644492683f18d')
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
    variant('krellpatch', default=False,
            description="Build with openspeedshop based patch.")
    variant('gtk',        default=False,
            description="Build with gtkplus.")
    variant('webkit',     default=False,
            description="Build the Webkit extension")
    variant('examples',   default=False,
            description="Build examples.")
    variant('dbus',       default=False,
            description="Build with D-Bus support.")
    variant('phonon',     default=False,
            description="Build with phonon support.")
    variant('opengl',     default=False,
            description="Build with OpenGL support.")

    # fix installation of pkgconfig files
    # see https://github.com/Homebrew/homebrew-core/pull/5951
    patch('restore-pc-files.patch', when='@5.9: platform=darwin')

    patch('qt3accept.patch', when='@3.3.8b')
    patch('qt3krell.patch', when='@3.3.8b+krellpatch')
    patch('qt3ptrdiff.patch', when='@3.3.8b')

    # see https://bugreports.qt.io/browse/QTBUG-57656
    patch('QTBUG-57656.patch', when='@5.8.0')
    # see https://bugreports.qt.io/browse/QTBUG-58038
    patch('QTBUG-58038.patch', when='@5.8.0')

    # https://github.com/xboxdrv/xboxdrv/issues/188
    patch('btn_trigger_happy.patch', when='@5.7.0:')

    # https://github.com/spack/spack/issues/1517
    patch('qt5-pcre.patch', when='@5:')

    patch('qt4-corewlan-new-osx.patch', when='@4')
    patch('qt4-pcre-include-conflict.patch', when='@4')
    patch('qt4-el-capitan.patch', when='@4')

    # Use system openssl for security.
    depends_on("openssl")
    depends_on("glib", when='@4:')
    depends_on("gtkplus", when='+gtk')
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("dbus", when='@4:+dbus')
    depends_on("libtiff")
    depends_on("libpng@1.2.57", when='@3')
    depends_on("libpng", when='@4:')
    depends_on("libmng")
    depends_on("jpeg")
    depends_on("icu4c")
    depends_on("fontconfig", when=(sys.platform != 'darwin'))  # (Unix only)
    depends_on("freetype")

    # Core options:
    # -doubleconversion  [system/qt/no]
    # -iconv             [posix/sun/gnu/no] (Unix only)
    # -pcre              [system/qt]

    # Gui, printing, widget options:
    # -harfbuzz          [system/qt/no]
    # -xkbcommon-x11     [system/qt/no]
    # -system-xkbcommon

    # Database options:
    # -sqlite            [system/qt]

    # Qt3D options:
    # -assimp            [system/qt/no]

    # QtQml
    depends_on("python", when='@5.7.0:', type='build')

    # OpenGL hardware acceleration
    depends_on("gl@3.2:", when='@4:+opengl')
    depends_on("libxcb", when=sys.platform != 'darwin')
    depends_on("libx11", when=sys.platform != 'darwin')

    if sys.platform != 'darwin':
        depends_on("libxext", when='@3:4.99')

    # Webkit
    depends_on("flex", when='+webkit', type='build')
    depends_on("bison", when='+webkit', type='build')
    depends_on("gperf", when='+webkit')

    # Multimedia
    # depends_on("gstreamer", when='+multimedia')
    # depends_on("pulse", when='+multimedia')
    # depends_on("flac", when='+multimedia')
    # depends_on("ogg", when='+multimedia')
    # -pulseaudio                [auto] (Unix only)
    # -alsa                      [auto] (Unix only)

    # Webengine options:
    # -webengine-alsa            [auto] (Linux only)
    # -webengine-pulseaudio      [auto] (Linux only)
    # -webengine-embedded-build  [auto] (Linux only)
    # -webengine-icu             [system/qt] (Linux only)
    # -webengine-ffmpeg          [system/qt] (Linux only)
    # -webengine-opus            [system/qt] (Linux only)
    # -webengine-webp            [system/qt] (Linux only)

    use_xcode = True

    def url_for_version(self, version):
        # URL keeps getting more complicated with every release
        url = self.list_url

        if version >= Version('4.0'):
            url += str(version.up_to(2)) + '/'
        else:
            url += str(version.up_to(1)) + '/'

        if version >= Version('4.8'):
            url += str(version) + '/'

        if version >= Version('5'):
            url += 'single/'

        url += 'qt-'

        if version >= Version('4.6'):
            url += 'everywhere-'
        elif version >= Version('2.1'):
            url += 'x11-'

        if version >= Version('5.10.0'):
            url += 'src-'
        elif version >= Version('4.0'):
            url += 'opensource-src-'
        elif version >= Version('3'):
            url += 'free-'

        # 5.9 only has xz format. From 5.2.1 -> 5.8.0 .gz or .xz were possible
        if version >= Version('5.9'):
            url += str(version) + '.tar.xz'
        else:
            url += str(version) + '.tar.gz'

        return url

    def setup_environment(self, spack_env, run_env):
        spack_env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))
        run_env.set('QTDIR', self.prefix)

    def setup_dependent_environment(self, spack_env, run_env, dependent_spec):
        spack_env.set('QTDIR', self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

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
        # incomplete list is here http://doc.qt.io/qt-5/configure-options.html
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-{0}opengl'.format('' if '+opengl' in self.spec else 'no-'),
            '-release',
            '-shared',
            '-confirm-license',
            '-openssl-linked',
            '-optimized-qmake',
            '-system-freetype',
            '-I{0}/freetype2'.format(self.spec['freetype'].prefix.include),
            '-no-pch'
        ]

        if sys.platform != 'darwin':
            config_args.append('-fontconfig')

        if '@:5.7.1' in self.spec:
            config_args.append('-no-openvg')
        else:
            # FIXME: those could work for other versions
            config_args.extend([
                '-system-libpng',
                '-system-libjpeg',
                '-system-zlib'
            ])

        if '@:5.7.0' in self.spec:
            config_args.extend([
                # NIS is deprecated in more recent glibc,
                # but qt-5.7.1 does not recognize this option
                '-no-nis',
            ])

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'examples'])

        if '@4' in self.spec and '~phonon' in self.spec:
            config_args.append('-no-phonon')

        if '+dbus' in self.spec:
            dbus = self.spec['dbus'].prefix
            config_args.append('-dbus-linked')
            config_args.append('-I%s/dbus-1.0/include' % dbus.lib)
            config_args.append('-I%s/dbus-1.0' % dbus.include)
            config_args.append('-L%s' % dbus.lib)
            config_args.append('-ldbus-1')
        else:
            config_args.append('-no-dbus')

        if '@5:' in self.spec and sys.platform == 'darwin':
            config_args.extend([
                '-no-xinput2',
                '-no-xcb-xlib',
                '-no-pulseaudio',
                '-no-alsa',
            ])

        # FIXME: else: -system-xcb ?

        if '@4' in self.spec and sys.platform == 'darwin':
            config_args.append('-cocoa')

            mac_ver = tuple(platform.mac_ver()[0].split('.')[:2])
            sdkname = 'macosx%s' % '.'.join(mac_ver)
            sdkpath = which('xcrun')('--show-sdk-path',
                                     '--sdk', sdkname,
                                     output=str)
            config_args.extend([
                '-sdk', sdkpath.strip(),
            ])
            use_clang_platform = False
            if self.spec.compiler.name == 'clang' and \
               str(self.spec.compiler.version).endswith('-apple'):
                use_clang_platform = True
            # No one uses gcc-4.2.1 anymore; this is clang.
            if self.spec.compiler.name == 'gcc' and \
               str(self.spec.compiler.version) == '4.2.1':
                use_clang_platform = True
            if use_clang_platform:
                config_args.append('-platform')
                if mac_ver >= (10, 9):
                    config_args.append('unsupported/macx-clang-libc++')
                else:
                    config_args.append('unsupported/macx-clang')

        return config_args

    # Don't disable all the database drivers, but should
    # really get them into spack at some point.

    @when('@3')
    def configure(self):
        # A user reported that this was necessary to link Qt3 on ubuntu.
        # However, if LD_LIBRARY_PATH is not set the qt build fails, check
        # and set LD_LIBRARY_PATH if not set, update if it is set.
        if os.environ.get('LD_LIBRARY_PATH'):
            os.environ['LD_LIBRARY_PATH'] += os.pathsep + os.getcwd() + '/lib'
        else:
            os.environ['LD_LIBRARY_PATH'] = os.pathsep + os.getcwd() + '/lib'

        configure('-prefix', self.prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast')

    @when('@4')
    def configure(self):
        configure('-fast',
                  '-{0}gtkstyle'.format('' if '+gtk' in self.spec else 'no-'),
                  '-{0}webkit'.format('' if '+webkit' in self.spec else 'no-'),
                  '-arch', str(self.spec.architecture.target),
                  *self.common_config_args)

    @when('@5.0:5.6')
    def configure(self):
        webkit_args = [] if '+webkit' in self.spec else ['-skip', 'qtwebkit']
        configure('-no-eglfs',
                  '-no-directfb',
                  '-{0}gtkstyle'.format('' if '+gtk' in self.spec else 'no-'),
                  *(webkit_args + self.common_config_args))

    @when('@5.7:')
    def configure(self):
        config_args = self.common_config_args

        if not sys.platform == 'darwin':
            config_args.extend([
                '-qt-xcb',
            ])

        if '~webkit' in self.spec:
            config_args.extend([
                '-skip', 'webengine',
            ])

        if '~opengl' in self.spec and self.spec.satisfies('@5.10:'):
            config_args.extend([
                '-skip', 'webglplugin',
            ])

        if self.version > Version('5.8'):
            # relies on a system installed wayland, i.e. no spack package yet
            # https://wayland.freedesktop.org/ubuntu16.04.html
            # https://wiki.qt.io/QtWayland
            config_args.extend(['-skip', 'wayland'])

        configure('-no-eglfs',
                  '-no-directfb',
                  '-{0}gtk'.format('' if '+gtk' in self.spec else 'no-'),
                  *config_args)

    def install(self, spec, prefix):
        self.configure()
        make()
        make("install")
