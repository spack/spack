# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
from spack.operating_systems.mac_os import macos_version
import os
import sys

MACOS_VERSION = macos_version() if sys.platform == 'darwin' else None


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'http://qt.io'
    # Alternative location 'http://download.qt.io/official_releases/qt/'
    url      = 'http://download.qt.io/archive/qt/5.7/5.7.0/single/qt-everywhere-opensource-src-5.7.0.tar.gz'
    list_url = 'http://download.qt.io/archive/qt/'
    list_depth = 3

    phases = ['configure', 'build', 'install']

    version('5.13.1', sha256='adf00266dc38352a166a9739f1a24a1e36f1be9c04bf72e16e142a256436974e')
    version('5.12.5', sha256='a2299e21db7767caf98242767bffb18a2a88a42fee2d6a393bedd234f8c91298')
    version('5.12.2', sha256='59b8cb4e728450b21224dcaaa40eb25bafc5196b6988f2225c394c6b7f881ff5')
    version('5.11.3', sha256='859417642713cee2493ee3646a7fee782c9f1db39e41d7bb1322bba0c5f0ff4d')
    version('5.11.2', sha256='c6104b840b6caee596fa9a35bc5f57f67ed5a99d6a36497b6fe66f990a53ca81')
    version('5.10.0', sha256='936d4cf5d577298f4f9fdb220e85b008ae321554a5fcd38072dc327a7296230e')
    version('5.9.1',  sha256='7b41a37d4fe5e120cdb7114862c0153f86c07abbec8db71500443d2ce0c89795')
    version('5.9.0',  sha256='f70b5c66161191489fc13c7b7eb69bf9df3881596b183e7f6d94305a39837517')
    version('5.8.0',  sha256='9dc5932307ae452855863f6405be1f7273d91173dcbe4257561676a599bd58d3')
    version('5.7.1',  sha256='c86684203be61ae7b33a6cf33c23ec377f246d697bd9fb737d16f0ad798f89b7')
    version('5.7.0',  sha256='4661905915d6265243e17fe59852930a229cf5b054ce5af5f48b34da9112ab5f')
    version('5.5.1',  sha256='c7fad41a009af1996b62ec494e438aedcb072b3234b2ad3eeea6e6b1f64be3b3')
    version('5.4.2',  sha256='cfc768c55f0a0cd232bed914a9022528f8f2e50cb010bf0e4f3f62db3dfa17bd')
    version('5.4.0',  sha256='1739633424bde3d89164ae6ff1c5c913be38b9997e451558ef873aac4bbc408a')
    version('5.3.2',  sha256='c8d3fd2ead30705c6673c5e4af6c6f3973346b4fb2bd6079c7be0943a5b0282d')
    version('5.2.1',  sha256='84e924181d4ad6db00239d87250cc89868484a14841f77fb85ab1f1dbdcd7da1')
    version('4.8.7',  sha256='e2882295097e47fe089f8ac741a95fef47e0a73a3f3cdf21b56990638f626ea0')
    version('4.8.6',  sha256='8b14dd91b52862e09b8e6a963507b74bc2580787d171feda197badfa7034032c')
    version('4.8.5',  sha256='eb728f8268831dc4373be6403b7dd5d5dde03c169ad6882f9a8cb560df6aa138')
    version('3.3.8b', sha256='1b7a1ff62ec5a9cb7a388e2ba28fda6f960b27f27999482ebeceeadb72ac9f6e')

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
    variant('framework',   default=bool(MACOS_VERSION),
            description="Build as a macOS Framework package.")
    variant('tools',      default=True,
            description="Build tools, including Qt Designer.")
    variant('dbus',       default=False,
            description="Build with D-Bus support.")
    variant('phonon',     default=False,
            description="Build with phonon support.")
    variant('opengl',     default=False,
            description="Build with OpenGL support.")
    variant('sql',        default=True,
            description="Build with SQL support.")
    variant('shared',     default=True,
            description='Build shared libraries.')
    variant('ssl',    default=True,
            description="Build with OpenSSL support.")
    variant('freetype', default='spack', description='Freetype2 support',
            values=('spack', 'qt', 'none'), multi=False)

    # fix installation of pkgconfig files
    # see https://github.com/Homebrew/homebrew-core/pull/5951
    patch('restore-pc-files.patch', when='@5.9:5.11 platform=darwin')

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

    patch('qt4-pcre-include-conflict.patch', when='@4.8.6')
    patch('qt4-tools.patch', when='@4+tools')
    if not MACOS_VERSION:
        # Allow Qt's configure script to build the webkit option with more
        # recent versions of gcc.
        # https://github.com/spack/spack/issues/9205
        # https://github.com/spack/spack/issues/9209
        patch('qt4-gcc-and-webkit.patch', when='@4:4.8.6')
        patch('qt4-gcc-and-webkit-487.patch', when='@4.8.7')
    else:
        patch('qt4-mac.patch', when='@4.8.7')

    # Fix build failure with newer versions of GCC
    patch('https://github.com/qt/qtbase/commit/a52d7861edfb5956de38ba80015c4dd0b596259b.patch',
          sha256='c49b228c27e3ad46ec3af4bac0e9985af5b5b28760f238422d32e14f98e49b1e',
          working_dir='qtbase',
          when='@5.10:5.12.0 %gcc@9:')

    # Fix build of QT4 with GCC 9
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=925811
    patch("qt4-gcc9-qforeach.patch", when="@4:4.999 %gcc@9")

    # https://bugreports.qt.io/browse/QTBUG-74196
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=89585
    patch('qt4-gcc8.3-asm-volatile-fix.patch', when='@4')
    patch('qt5-gcc8.3-asm-volatile-fix.patch', when='@5.0.0:5.12.1')

    # patch overflow builtins
    patch('qt5_11-intel-overflow.patch', when='@5.11')
    patch('qt5_12-intel-overflow.patch', when='@5.12:')

    # Build-only dependencies
    depends_on("pkgconfig", type='build')
    depends_on("flex", when='+webkit', type='build')
    depends_on("bison", when='+webkit', type='build')
    depends_on("python", when='@5.7.0:', type='build')

    # Dependencies, then variant- and version-specific dependencies
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on("libmng")
    depends_on("libtiff")
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("freetype", when='freetype=spack')
    depends_on("gperf", when='+webkit')
    depends_on("gtkplus", when='+gtk')
    depends_on("openssl", when='+ssl')
    depends_on("sqlite", when='+sql', type=('build', 'run'))
    depends_on("sqlite+column_metadata", when='+sql%intel', type=('build', 'run'))

    depends_on("libpng@1.2.57", when='@3')
    depends_on("pcre+multibyte", when='@5.0:5.8')
    depends_on("inputproto", when='@:5.8')
    depends_on("openssl@:1.0.999", when='@:5.9+ssl~krellpatch')

    depends_on("glib", when='@4:')
    depends_on("libpng", when='@4:')
    depends_on("dbus", when='@4:+dbus')
    depends_on("gl@3.2:", when='@4:+opengl')

    depends_on("harfbuzz", when='@5:')
    depends_on("double-conversion", when='@5.7:')
    depends_on("pcre2+multibyte", when='@5.9:')

    # Non-macOS dependencies and special macOS constraints
    if MACOS_VERSION is None:
        depends_on("fontconfig", when='freetype=spack')
        depends_on("libx11")
        depends_on("libxcb")
        depends_on("libxkbcommon")
        depends_on("xcb-util-image")
        depends_on("xcb-util-keysyms")
        depends_on("xcb-util-renderutil")
        depends_on("xcb-util-wm")
        depends_on("libxext")
        depends_on("libxrender")
        conflicts('+framework',
                  msg="QT cannot be built as a framework except on macOS.")
    else:
        conflicts('platform=darwin', when='@4.8.6',
                  msg="QT 4 for macOS is only patched for 4.8.7")

    use_xcode = True

    # Mapping for compilers in the QT 'mkspecs'
    compiler_mapping = {'intel': 'icc', 'clang': 'clang-libc++', 'gcc': 'g++'}

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

    def setup_build_environment(self, env):
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))

    def setup_run_environment(self, env):
        env.set('QTDIR', self.prefix)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('QTDIR', self.prefix)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

    @when('@4 platform=darwin')
    def patch(self):
        ogl = self.spec['opengl'] if '+opengl' in self.spec else None
        deployment_target = str(MACOS_VERSION.up_to(2))

        patches = {
            'MACOSX_DEPLOYMENT_TARGET': deployment_target,
            'PREFIX': self.prefix,
            'OPENGL_INCDIR': ogl.prefix.include if ogl else "",
            'OPENGL_LIBS': ogl.libs.ld_flags if ogl else "",
        }

        def repl(match):
            # Replace the original config variable value with the one chosen
            # here if it is mentioned in 'patches'; otherwise return the
            # original value.
            return patches.get(match.group(1), match.group(0))

        files_to_filter = [
            "configure",
            "mkspecs/common/mac.conf",
            "mkspecs/common/unix.conf",
            "mkspecs/common/gcc-base-macx.conf",
            "mkspecs/common/gcc-base.conf",
            "qmake/generators/unix/unixmake.cpp",
            "qmake/qmake.pri",
            "src/tools/bootstrap/bootstrap.pro"
        ]
        if '%clang' in self.spec:
            files_to_filter += [
                "mkspecs/unsupported/macx-clang-libc++/qmake.conf",
                "mkspecs/common/clang.conf"
            ]
        elif '%gcc' in self.spec:
            files_to_filter += [
                "mkspecs/common/g++-macx.conf",
                "mkspecs/darwin-g++/qmake.conf"
            ]

        # Filter inserted configure variables
        filter_file(r'@([a-zA-Z0-9_]+)@', repl, *files_to_filter)

        # Remove debug build
        files_to_filter = [
            "src/3rdparty/webkit/Source/WebKit.pri",
            "src/3rdparty/webkit/Source/WebKit/qt/declarative/declarative.pro",
            "src/imports/qimportbase.pri",
            "src/plugins/qpluginbase.pri",
            "src/qbase.pri",
            "tools/designer/src/components/lib/lib.pro",
            "tools/designer/src/lib/lib.pro",
            "tools/designer/src/plugins/activeqt/activeqt.pro",
            "tools/designer/src/plugins/plugins.pri",
            "tools/designer/src/uitools/uitools.pro",
        ]
        filter_file(r'(\+=.*)debug_and_release', r'\1', *files_to_filter)

    @when('@4')  # *NOT* darwin/mac
    def patch(self):
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

    @when('@5')
    def patch(self):
        # Fix qmake compilers in the default mkspec
        filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc',
                    'qtbase/mkspecs/common/g++-base.conf')
        filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++',
                    'qtbase/mkspecs/common/g++-base.conf')

        filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                    'qtbase/mkspecs/common/g++-unix.conf')

    @property
    def common_config_args(self):
        # incomplete list is here http://doc.qt.io/qt-5/configure-options.html
        openssl = self.spec['openssl']
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-{0}opengl'.format('' if '+opengl' in self.spec else 'no-'),
            '-release',
            '-confirm-license',
            '-openssl-linked',
            openssl.libs.search_flags,
            openssl.headers.include_flags,
            '-optimized-qmake',
            '-no-pch',
        ]

        if self.spec.variants['freetype'].value == 'spack':
            config_args.extend([
                '-system-freetype',
                '-I{0}/freetype2'.format(self.spec['freetype'].prefix.include)
            ])
            if not MACOS_VERSION:
                config_args.append('-fontconfig')

        elif self.spec.variants['freetype'].value == 'qt':
            config_args.append('-qt-freetype')
        else:
            config_args.append('-no-freetype')

        if '+ssl' in self.spec:
            config_args.append('-openssl-linked')
        else:
            config_args.append('-no-openssl')

        if '+sql' in self.spec:
            sqlite = self.spec['sqlite']
            config_args.extend([
                '-system-sqlite',
                '-R', sqlite.prefix.lib,
            ])
        else:
            comps = ['db2', 'ibase', 'oci', 'tds', 'mysql', 'odbc', 'psql',
                     'sqlite', 'sqlite2']
            config_args.extend("-no-sql-" + component for component in comps)

        if '+shared' in self.spec:
            config_args.append('-shared')
        else:
            config_args.append('-static')

        if self.spec.satisfies('@5:'):
            pcre = self.spec['pcre'] if self.spec.satisfies('@5.0:5.8') \
                else self.spec['pcre2']
            harfbuzz = self.spec['harfbuzz']
            config_args.extend([
                '-system-harfbuzz',
                harfbuzz.libs.search_flags,
                harfbuzz.headers.include_flags,
                '-system-pcre',
                pcre.libs.search_flags,
                pcre.headers.include_flags
            ])

        if self.spec.satisfies('@5.7:'):
            dc = self.spec['double-conversion']
            config_args.extend([
                '-system-doubleconversion',
                dc.libs.search_flags,
                dc.headers.include_flags
            ])

        if '@:5.7.1' in self.spec:
            config_args.append('-no-openvg')
        else:
            # FIXME: those could work for other versions
            png = self.spec['libpng']
            config_args.append('-system-libpng')
            if not png.external:
                config_args.extend([
                    png.libs.search_flags,
                    png.headers.include_flags
                ])

            jpeg = self.spec['jpeg']
            config_args.append('-system-libjpeg')
            if not jpeg.external:
                config_args.extend([
                    jpeg.libs.search_flags,
                    jpeg.headers.include_flags,
                ])
            zlib = self.spec['zlib']
            config_args.append('-system-zlib')
            if not zlib.external:
                config_args.extend([
                    zlib.libs.search_flags,
                    zlib.headers.include_flags
                ])

        if '@:5.7.0' in self.spec:
            config_args.extend([
                # NIS is deprecated in more recent glibc,
                # but qt-5.7.1 does not recognize this option
                '-no-nis',
            ])

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'examples'])

        if '~tools' in self.spec:
            config_args.extend(['-nomake', 'tools'])

        if '+dbus' in self.spec:
            dbus = self.spec['dbus'].prefix
            config_args.append('-dbus-linked')
            config_args.append('-I%s/dbus-1.0/include' % dbus.lib)
            config_args.append('-I%s/dbus-1.0' % dbus.include)
            config_args.append('-L%s' % dbus.lib)
        else:
            config_args.append('-no-dbus')

        if MACOS_VERSION:
            config_args.append('-{0}framework'.format(
                '' if '+framework' in self.spec else 'no-'))

        # Note: QT defaults to the following compilers
        #  QT4 mac: gcc
        #  QT5 mac: clang
        #  linux: gcc
        # In QT4, unsupported compilers lived under an 'unsupported'
        # subdirectory but are now in the main platform directory.
        spec = self.spec
        cname = spec.compiler.name
        cname = self.compiler_mapping.get(cname, cname)
        is_new_qt = spec.satisfies('@5:')
        platform = None
        if MACOS_VERSION:
            if is_new_qt and cname != "clang-libc++":
                platform = 'macx-' + cname
            elif not is_new_qt and cname != "g++":
                platform = 'unsupported/macx-' + cname
        elif cname != 'g++':
            if is_new_qt:
                platform = 'linux-' + cname
            else:
                platform = 'unsupported/linux-' + cname

        if platform is not None:
            config_args.extend(['-platform', platform])

        return config_args

    # Don't disable all the database drivers, but should
    # really get them into spack at some point.

    @when('@3')
    def configure(self, spec, prefix):
        # A user reported that this was necessary to link Qt3 on ubuntu.
        # However, if LD_LIBRARY_PATH is not set the qt build fails, check
        # and set LD_LIBRARY_PATH if not set, update if it is set.
        if os.environ.get('LD_LIBRARY_PATH'):
            os.environ['LD_LIBRARY_PATH'] += os.pathsep + os.getcwd() + '/lib'
        else:
            os.environ['LD_LIBRARY_PATH'] = os.pathsep + os.getcwd() + '/lib'

        configure('-prefix', prefix,
                  '-v',
                  '-thread',
                  '-shared',
                  '-release',
                  '-fast')

    @when('@4')
    def configure(self, spec, prefix):
        config_args = self.common_config_args

        config_args.extend([
            '-fast',
            '-no-declarative-debug',
            '-{0}gtkstyle'.format('' if '+gtk' in spec else 'no-'),
            '-{0}webkit'.format('' if '+webkit' in spec else 'no-'),
            '-{0}phonon'.format('' if '+phonon' in spec else 'no-'),
            '-arch', str(spec.target.family),
        ])

        # Disable phonon backend until gstreamer is setup as dependency
        if '+phonon' in self.spec:
            config_args.append('-no-phonon-backend')

        if '~examples' in self.spec:
            config_args.extend(['-nomake', 'demos'])

        if MACOS_VERSION:
            sdkpath = which('xcrun')('--show-sdk-path', output=str).strip()
            config_args.extend([
                '-cocoa',
                '-sdk', sdkpath])

        configure(*config_args)

    @when('@5')
    def configure(self, spec, prefix):
        config_args = self.common_config_args
        version = self.version

        config_args.extend([
            '-no-eglfs',
            '-no-directfb',
            '-{0}gtk{1}'.format(
                '' if '+gtk' in spec else 'no-',
                '' if version >= Version('5.7') else 'style')
        ])

        if MACOS_VERSION:
            config_args.extend([
                '-no-xcb-xlib',
                '-no-pulseaudio',
                '-no-alsa',
            ])
            if version < Version('5.12'):
                config_args.append('-no-xinput2')
        else:
            # Linux-only QT5 dependencies
            config_args.append('-system-xcb')

        if '~webkit' in spec:
            config_args.extend([
                '-skip',
                'webengine' if version >= Version('5.7') else 'qtwebkit',
            ])

        if spec.satisfies('@5.7'):
            config_args.extend(['-skip', 'virtualkeyboard'])

        if version >= Version('5.8'):
            # relies on a system installed wayland, i.e. no spack package yet
            # https://wayland.freedesktop.org/ubuntu16.04.html
            # https://wiki.qt.io/QtWayland
            config_args.extend(['-skip', 'wayland'])

        if version >= Version('5.10') and '~opengl' in spec:
            config_args.extend([
                '-skip', 'webglplugin',
            ])

        configure(*config_args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")
