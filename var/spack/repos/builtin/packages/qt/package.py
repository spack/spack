# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
import itertools
import os
import platform
import sys

import llnl.util.tty as tty

from spack import *
from spack.operating_systems.linux_distro import kernel_version
from spack.operating_systems.mac_os import macos_version

MACOS_VERSION = macos_version() if sys.platform == 'darwin' else None
LINUX_VERSION = kernel_version() if platform.system() == 'Linux' else None


class Qt(Package):
    """Qt is a comprehensive cross-platform C++ application framework."""
    homepage = 'https://qt.io'

    # Supported releases: 'https://download.qt.io/official_releases/qt/'
    # Older archives: 'https://download.qt.io/new_archive/qt/'
    url      = 'https://download.qt.io/archive/qt/5.15/5.15.2/single/qt-everywhere-src-5.15.2.tar.xz'
    list_url = 'https://download.qt.io/archive/qt/'
    list_depth = 3
    maintainers = ['sethrj']

    phases = ['configure', 'build', 'install']

    version('5.15.4', sha256='615ff68d7af8eef3167de1fd15eac1b150e1fd69d1e2f4239e54447e7797253b')
    version('5.15.3', sha256='b7412734698a87f4a0ae20751bab32b1b07fdc351476ad8e35328dbe10efdedb')
    version('5.15.2', sha256='3a530d1b243b5dec00bc54937455471aaa3e56849d2593edb8ded07228202240')
    version('5.14.2', sha256='c6fcd53c744df89e7d3223c02838a33309bd1c291fcb6f9341505fe99f7f19fa')
    version('5.14.1', sha256='6f17f488f512b39c2feb57d83a5e0a13dcef32999bea2e2a8f832f54a29badb8', deprecated=True)
    version('5.14.0', sha256='be9a77cd4e1f9d70b58621d0753be19ea498e6b0da0398753e5038426f76a8ba', deprecated=True)
    version('5.13.1', sha256='adf00266dc38352a166a9739f1a24a1e36f1be9c04bf72e16e142a256436974e', deprecated=True)
    version('5.12.10', sha256='3e0ee1e57f5cf3eeb038d0b4b22c7eb442285c62639290756b39dc93a1d0e14f')
    version('5.12.7', sha256='873783a0302129d98a8f63de9afe4520fb5f8d5316be8ad7b760c59875cd8a8d', deprecated=True)
    version('5.12.5', sha256='a2299e21db7767caf98242767bffb18a2a88a42fee2d6a393bedd234f8c91298', deprecated=True)
    version('5.12.2', sha256='59b8cb4e728450b21224dcaaa40eb25bafc5196b6988f2225c394c6b7f881ff5', deprecated=True)
    version('5.11.3', sha256='859417642713cee2493ee3646a7fee782c9f1db39e41d7bb1322bba0c5f0ff4d', deprecated=True)
    version('5.11.2', sha256='c6104b840b6caee596fa9a35bc5f57f67ed5a99d6a36497b6fe66f990a53ca81', deprecated=True)
    version('5.10.0', sha256='936d4cf5d577298f4f9fdb220e85b008ae321554a5fcd38072dc327a7296230e', deprecated=True)
    version('5.9.9',  sha256='5ce285209290a157d7f42ec8eb22bf3f1d76f2e03a95fc0b99b553391be01642')
    version('5.9.1',  sha256='7b41a37d4fe5e120cdb7114862c0153f86c07abbec8db71500443d2ce0c89795', deprecated=True)
    version('5.9.0',  sha256='f70b5c66161191489fc13c7b7eb69bf9df3881596b183e7f6d94305a39837517', deprecated=True)
    version('5.8.0', sha256='0f4c54386d3dbac0606a936a7145cebb7b94b0ca2d29bc001ea49642984824b6', deprecated=True)
    version('5.7.1', sha256='46ebca977deb629c5e69c2545bc5fe13f7e40012e5e2e451695c583bd33502fa', deprecated=True)
    version('5.7.0', sha256='a6a2632de7e44bbb790bc3b563f143702c610464a7f537d02036749041fd1800', deprecated=True)
    version('5.6.3',  sha256='2fa0cf2e5e8841b29a4be62062c1a65c4f6f2cf1beaf61a5fd661f520cd776d0')
    version('5.5.1',  sha256='c7fad41a009af1996b62ec494e438aedcb072b3234b2ad3eeea6e6b1f64be3b3', deprecated=True)
    version('5.4.2',  sha256='cfc768c55f0a0cd232bed914a9022528f8f2e50cb010bf0e4f3f62db3dfa17bd', deprecated=True)
    version('5.4.0',  sha256='1739633424bde3d89164ae6ff1c5c913be38b9997e451558ef873aac4bbc408a', deprecated=True)
    version('5.3.2',  sha256='c8d3fd2ead30705c6673c5e4af6c6f3973346b4fb2bd6079c7be0943a5b0282d')
    version('5.2.1',  sha256='84e924181d4ad6db00239d87250cc89868484a14841f77fb85ab1f1dbdcd7da1')
    version('4.8.7',  sha256='e2882295097e47fe089f8ac741a95fef47e0a73a3f3cdf21b56990638f626ea0')
    version('4.8.6',  sha256='8b14dd91b52862e09b8e6a963507b74bc2580787d171feda197badfa7034032c')
    version('4.8.5',  sha256='eb728f8268831dc4373be6403b7dd5d5dde03c169ad6882f9a8cb560df6aa138')
    version('3.3.8b', sha256='1b7a1ff62ec5a9cb7a388e2ba28fda6f960b27f27999482ebeceeadb72ac9f6e')

    variant('debug',      default=False,
            description="Build debug version.")
    variant('dbus',       default=False,
            description="Build with D-Bus support.")
    variant('doc',      default=False,
            description="Build QDoc and documentation.")
    variant('examples',   default=False,
            description="Build examples.")
    variant('framework',   default=bool(MACOS_VERSION),
            description="Build as a macOS Framework package.")
    variant('gtk',        default=False,
            description="Build with gtkplus.")
    variant('gui', default=True,
            description='Build the Qt GUI module and dependencies')
    variant('opengl',     default=False,
            description="Build with OpenGL support.")
    variant('phonon',     default=False,
            description="Build with phonon support.")
    variant('shared',     default=True,
            description='Build shared libraries.')
    variant('sql',        default=True,
            description="Build with SQL support.")
    variant('ssl',    default=True,
            description="Build with OpenSSL support.")
    variant('tools',      default=True,
            description="Build tools, including Qt Designer.")
    variant('webkit',     default=False,
            description="Build the Webkit extension")

    # Patches for qt@3
    patch('qt3-accept.patch', when='@3')
    patch('qt3-headers.patch', when='@3')

    # Patches for qt@4
    patch('qt4-configure-gcc.patch', when='@4:4.8.6 %gcc')
    patch('qt4-87-configure-gcc.patch', when='@4.8.7 %gcc')
    patch('qt4-tools.patch', when='@4+tools')
    patch('qt4-mac.patch', when='@4.8.7 platform=darwin')
    # https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=925811
    patch("qt4-qforeach.patch", when="@4 %gcc@9:")

    # Patches for qt@4:
    # https://github.com/spack/spack/issues/1517
    patch('qt4-pcre.patch', when='@4')
    patch('qt5-pcre.patch', when='@5:')
    # https://bugreports.qt.io/browse/QTBUG-74196
    # https://gcc.gnu.org/bugzilla/show_bug.cgi?id=89585
    patch('qt4-asm-volatile.patch', when='@4')
    patch('qt5-asm-volatile.patch', when='@5.0.0:5.12.1')

    # Patches for qt@5
    # https://bugreports.qt.io/browse/QTBUG-74219
    patch('qt5-btn_trigger_happy.patch', when='@5.7:5.12')
    # https://bugreports.qt.io/browse/QTBUG-57656
    patch('qt5-8-framework.patch', when='@5.8.0 +framework')
    # https://bugreports.qt.io/browse/QTBUG-58038
    patch('qt5-8-freetype.patch', when='@5.8.0 +gui')
    # https://codereview.qt-project.org/c/qt/qtbase/+/245425
    patch('https://github.com/qt/qtbase/commit/a52d7861edfb5956de38ba80015c4dd0b596259b.patch?full_index=1',
          sha256='c113b4e31fc648d15d6d401f7625909d84f88320172bd1fbc5b100cc2cbf71e9',
          working_dir='qtbase',
          when='@5.10:5.12.0 %gcc@9:')
    # https://github.com/Homebrew/homebrew-core/pull/5951
    patch('qt5-restore-pc-files.patch', when='@5.9:5.11 platform=darwin')
    # https://github.com/spack/spack/issues/14400
    patch('qt5-11-intel-overflow.patch', when='@5.11 %intel')
    patch('qt5-12-intel-overflow.patch', when='@5.12:5.14.0 %intel')
    # https://bugreports.qt.io/browse/QTBUG-78937
    patch('qt5-12-configure.patch', when='@5.12.7')
    # https://bugreports.qt.io/browse/QTBUG-93402
    patch('qt5-15-gcc-10.patch', when='@5.12.7:5.15 %gcc@8:')
    patch('qt514.patch', when='@5.14')
    patch('qt514-isystem.patch', when='@5.14.2')
    # https://bugreports.qt.io/browse/QTBUG-84037
    patch('qt515-quick3d-assimp.patch', when='@5.15:5+opengl')
    # https://bugreports.qt.io/browse/QTBUG-90395
    patch('https://src.fedoraproject.org/rpms/qt5-qtbase/raw/6ae41be8260f0f5403367eb01f7cd8319779674a/f/qt5-qtbase-gcc11.patch',
          sha256='9378afd071ad5c0ec8f7aef48421e4b9fab02f24c856bee9c0951143941913c5',
          working_dir='qtbase',
          when='@5.14: %gcc@11:')
    patch('https://src.fedoraproject.org/rpms/qt5-qtdeclarative/raw/593481a2541d3218f285dd7b46bdc5f4c76075ab/f/qt5-qtdeclarative-gcc11.patch',
          sha256='2081e9cb85f6712be9b63c70204efa3da954c07d857283eeae16d1b0409704bd',
          working_dir='qtdeclarative',
          when='@5.14: %gcc@11:')
    patch('https://src.fedoraproject.org/rpms/qt5-qtwebsockets/raw/f54f4ce6fa27941e9e6d606103d32056078edc74/f/qt5-qtwebsockets-gcc11.patch',
          sha256='84b099109d08adf177adf9d3542b6215ec3e42138041d523860dbfdcb59fdaae',
          working_dir='qtwebsockets',
          when='@5.14: %gcc@11:')
    # https://github.com/microsoft/vcpkg/issues/21055
    patch('qt5-macos12.patch',
          working_dir='qtbase',
          when='@5.14: %apple-clang@13:')

    # Spack path substitution uses excessively long paths that exceed the hard-coded
    # limit of 256 used by teh generated code with the prefix path as string literals
    # causing qt to fail in ci.  This increases that limit to 1024.
    patch('qt59-qtbase-qtconfig256.patch', working_dir='qtbase', when='@5.9:5')

    conflicts('%gcc@10:', when='@5.9:5.12.6 +opengl')
    conflicts('%gcc@11:', when='@5.8')
    conflicts('%apple-clang@13:', when='@:5.13')

    # Build-only dependencies
    depends_on("pkgconfig", type='build')
    depends_on("python", when='@5.7.0:', type='build')

    # Dependencies, then variant- and version-specific dependencies
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on("libmng")
    depends_on("libtiff")
    depends_on("libxml2")
    depends_on("zlib")
    depends_on("freetype", when='+gui')
    depends_on("gtkplus", when='+gtk')
    depends_on("sqlite+column_metadata", when='+sql', type=('build', 'run'))

    depends_on("libpng@1.2.57", when='@3')
    depends_on("libsm", when='@3')
    depends_on("pcre+multibyte", when='@5.0:5.8')
    depends_on("inputproto", when='@:5.8')

    with when('+ssl'):
        depends_on("openssl")
        depends_on("openssl@:1.0", when='@4:5.9')
        depends_on("openssl@1.1.1:", when='@5.15.0:')

    depends_on("glib", when='@4:')
    depends_on("libpng", when='@4:')
    depends_on("dbus", when='@4:+dbus')
    depends_on("gl", when='@4:+opengl')
    depends_on("assimp@5.0.0:5", when='@5.5:+opengl')

    depends_on("harfbuzz", when='@5:')
    depends_on("double-conversion", when='@5.7:')
    depends_on("pcre2+multibyte", when='@5.9:')
    depends_on("llvm", when='@5.11: +doc')
    depends_on("zstd@1.3:", when='@5.13:')

    with when('+webkit'):
        patch(
            'https://src.fedoraproject.org/rpms/qt5-qtwebengine/raw/32062243e895612823b47c2ae9eeb873a98a3542/f/qtwebengine-gcc11.patch',
            sha256='14e2d6baff0d09a528ee3e2b5a14de160859880360100af75ea17f3e0f672787',
            working_dir='qtwebengine',
            when='@5.15.2: %gcc@11:'
        )
        # the gl headers and dbus are needed to build webkit
        conflicts('~opengl')
        conflicts('~dbus')

        depends_on("flex", type='build')
        depends_on("bison", type='build')
        depends_on("gperf")

        # qtwebengine@5.7:5.15 are based on Google Chromium versions which depend on Py2
        with when('@5.7:5.15'):
            depends_on('python@2.7.5:2', type='build')
            # mesa inherits MesonPackage (since October 2020) which depends on Py@3.
            # The conflicts('mesa') enables a regular build of `qt@5.7:5.15+webkit`
            # without having to specify the exact version by causing the concretizer
            # to select mesa18 which does not depend on python@3.
            conflicts('mesa')

        with when('@5.10:'):
            depends_on('nss@3.62:')

        with when('@5.7:'):
            # https://www.linuxfromscratch.org/blfs/view/svn/x/qtwebengine.html
            depends_on('ninja', type='build')

        # https://doc.qt.io/qt-5.15/qtwebengine-platform-notes.html
        with when('@5.7: platform=linux'):
            depends_on("libdrm")
            depends_on("libxcomposite")
            depends_on("libxcursor")
            depends_on("libxi")
            depends_on("libxtst")
            depends_on("libxrandr")
            depends_on("libxdamage")
            depends_on("gettext")

    # gcc@4 is not supported as of Qt@5.14
    # https://doc.qt.io/qt-5.14/supported-platforms.html
    conflicts('%gcc@:4', when='@5.14:')

    # Non-macOS dependencies and special macOS constraints
    if MACOS_VERSION is None:
        with when('+gui'):
            depends_on("fontconfig")
            depends_on("libsm")
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
        conflicts('platform=darwin', when='@:4.8.6',
                  msg="QT 4 for macOS is only patched for 4.8.7")
        conflicts('target=aarch64:', when='@:5.15.3',
                  msg='Apple Silicon requires a very new version of qt')

    use_xcode = True

    # Mapping for compilers/systems in the QT 'mkspecs'
    compiler_mapping = {'intel': ('icc',),
                        'apple-clang': ('clang-libc++', 'clang'),
                        'clang': ('clang-libc++', 'clang'),
                        'fj': ('clang',),
                        'gcc': ('g++',)}
    platform_mapping = {'darwin': ('macx'), 'cray': ('linux')}

    def url_for_version(self, version):
        # URL keeps getting more complicated with every release
        url = self.list_url

        if version < Version('5.12') and version.up_to(2) != Version('5.9'):
            # As of 28 April 2021:
            # - new_archive contains 1-5.8, 5.10-5.11
            # - archive contains 1-5.1, 5.9, 5.12-6.0
            # - official_releases containis 5.9, 5.12, 5.15, 6.0
            url = url.replace('archive', 'new_archive')

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
            if version >= Version('5.15.3'):
                url += 'opensource-src-'
            else:
                url += 'src-'
        elif version >= Version('4.0'):
            url += 'opensource-src-'
        elif version >= Version('3'):
            url += 'free-'

        # 5.6.3 and 5.9 only has xz format. Some older versions have only .gz
        if version >= Version('5.6'):
            url += str(version) + '.tar.xz'
        else:
            url += str(version) + '.tar.gz'

        return url

    def setup_build_environment(self, env):
        env.set('MAKEFLAGS', '-j{0}'.format(make_jobs))
        if self.version >= Version('5.11'):
            # QDoc uses LLVM as of 5.11; remove the LLVM_INSTALL_DIR to
            # disable
            try:
                llvm_path = self.spec['llvm'].prefix
            except KeyError:
                # Prevent possibly incompatible system LLVM from being found
                llvm_path = "/spack-disable-llvm"
            env.set('LLVM_INSTALL_DIR', llvm_path)

    def setup_run_environment(self, env):
        env.set('QTDIR', self.prefix)
        env.set('QTINC', self.prefix.inc)
        env.set('QTLIB', self.prefix.lib)
        env.prepend_path('QT_PLUGIN_PATH', self.prefix.plugins)

    def setup_dependent_build_environment(self, env, dependent_spec):
        env.set('QTDIR', self.prefix)
        env.set('QTINC', self.prefix.inc)
        env.set('QTLIB', self.prefix.lib)
        env.prepend_path('QT_PLUGIN_PATH', self.prefix.plugins)

    def setup_dependent_package(self, module, dependent_spec):
        module.qmake = Executable(join_path(self.spec.prefix.bin, 'qmake'))

    def get_mkspec(self):
        """Determine the mkspecs root directory and QT platform.
        """
        spec = self.spec
        cname = spec.compiler.name
        pname = spec.architecture.platform

        # Transform spack compiler name to a list of possible QT compilers
        cnames = self.compiler_mapping.get(cname, [cname])
        # Transform platform name to match those in QT
        pname = self.platform_mapping.get(pname, pname)

        qtplat = None
        mkspec_dir = 'qtbase/mkspecs' if spec.satisfies('@5:') else 'mkspecs'
        for subdir, cname in itertools.product(('', 'unsupported/'), cnames):
            platdirname = "".join([subdir, pname, "-", cname])
            tty.debug("Checking for platform '{0}' in {1}".format(
                      platdirname, mkspec_dir))
            if os.path.exists(os.path.join(mkspec_dir, platdirname)):
                qtplat = platdirname
                break
        else:
            tty.warn("No matching QT platform was found in {0} "
                     "for platform '{1}' and compiler {2}".format(
                         mkspec_dir, pname, ",".join(cnames)))

        return (mkspec_dir, qtplat)

    # webkit requires libintl (gettext), but does not test for it
    # correctly, so add it here.
    def flag_handler(self, name, flags):
        if '+webkit' in self.spec and name == 'ldlibs':
            flags.append('-lintl')

        return (flags, None, None)

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
        if '%clang' in self.spec or '%apple-clang' in self.spec:
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

    @when('@4: %gcc')  # *NOT* darwin/mac gcc
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()

        def conf(name):
            return os.path.join(mkspec_dir, 'common', name + '.conf')

        # Fix qmake compilers in the default mkspec
        filter_file('^QMAKE_CC .*', 'QMAKE_CC = cc', conf('g++-base'))
        filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = c++', conf('g++-base'))

        # Don't error out on undefined symbols
        filter_file('^QMAKE_LFLAGS_NOUNDEF .*', 'QMAKE_LFLAGS_NOUNDEF = ',
                    conf('g++-unix'))

        # https://gcc.gnu.org/gcc-11/porting_to.html: add -include limits
        if self.spec.satisfies('@5.9:5.14%gcc@11:'):
            with open(conf('gcc-base'), 'a') as f:
                f.write("QMAKE_CXXFLAGS += -include limits\n")

        if self.spec.satisfies('@4'):
            # The gnu98 flag is necessary to build with GCC 6 and other modern
            # compilers (see http://stackoverflow.com/questions/10354371/);
            # be permissive because of the abundance of older code, and hide
            # all warnings because there are so many of them with newer
            # compilers
            with open(conf('gcc-base'), 'a') as f:
                f.write("QMAKE_CXXFLAGS += -std=gnu++98 -fpermissive -w\n")

    @when('@4: %intel')
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()
        conf_file = os.path.join(mkspec_dir, platform, "qmake.conf")

        # Intel's `ar` equivalent might not be in the path: replace it with
        # explicit
        xiar = os.path.join(os.path.dirname(self.compiler.cc), 'xiar')
        filter_file(r'\bxiar\b', xiar, conf_file)

        if self.spec.satisfies('@4'):
            with open(conf_file, 'a') as f:
                f.write("QMAKE_CXXFLAGS += -std=gnu++98\n")

    @when('@4 %clang')
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()
        conf_file = os.path.join(mkspec_dir, platform, "qmake.conf")

        with open(conf_file, 'a') as f:
            f.write("QMAKE_CXXFLAGS += -std=gnu++98\n")

    @when('@5.9 platform=darwin')
    def patch(self):
        # 'javascriptcore' is in the include path, so its file named 'version'
        # interferes with the standard library
        os.unlink(join_path(self.stage.source_path,
                            'qtscript/src/3rdparty/javascriptcore/version'))

    @when('@4: %fj')
    def patch(self):
        (mkspec_dir, platform) = self.get_mkspec()

        conf = os.path.join(mkspec_dir, 'common', 'clang.conf')

        # Fix qmake compilers in the default mkspec
        filter_file('^QMAKE_CC .*', 'QMAKE_CC = fcc', conf)
        filter_file('^QMAKE_CXX .*', 'QMAKE_CXX = FCC', conf)

        if self.spec.satisfies('@4'):
            conf_file = os.path.join(mkspec_dir, platform, "qmake.conf")
            with open(conf_file, 'a') as f:
                f.write("QMAKE_CXXFLAGS += -std=gnu++98\n")

    def _dep_appender_factory(self, config_args):
        spec = self.spec

        def use_spack_dep(spack_pkg, qt_name=None):
            pkg = spec[spack_pkg]
            config_args.append('-system-' + (qt_name or spack_pkg))
            if not pkg.external:
                config_args.extend(pkg.libs.search_flags.split())
                config_args.extend(pkg.headers.include_flags.split())
        return use_spack_dep

    @property
    def common_config_args(self):
        spec = self.spec
        version = self.version

        # incomplete list is here https://doc.qt.io/qt-5/configure-options.html
        config_args = [
            '-prefix', self.prefix,
            '-v',
            '-opensource',
            '-{0}opengl'.format('' if '+opengl' in spec else 'no-'),
            '-{0}'.format('debug' if '+debug' in spec else 'release'),
            '-confirm-license',
            '-optimized-qmake',
            '-no-pch',
        ]

        use_spack_dep = self._dep_appender_factory(config_args)

        if '+gui' in spec:
            use_spack_dep('freetype')
            if not MACOS_VERSION:
                config_args.append('-fontconfig')
        else:
            config_args.append('-no-freetype')
            config_args.append('-no-gui')

        if '+ssl' in spec:
            pkg = spec['openssl']
            config_args.append('-openssl-linked')
            config_args.extend(pkg.libs.search_flags.split())
            config_args.extend(pkg.headers.include_flags.split())
        else:
            config_args.append('-no-openssl')

        if '+sql' in spec:
            use_spack_dep('sqlite')
        else:
            comps = ['db2', 'ibase', 'oci', 'tds', 'mysql', 'odbc', 'psql',
                     'sqlite', 'sqlite2']
            config_args.extend("-no-sql-" + component for component in comps)

        if '+shared' in spec:
            config_args.append('-shared')
        else:
            config_args.append('-static')

        if version >= Version('5'):
            use_spack_dep('pcre' if spec.satisfies('@5.0:5.8') else 'pcre2',
                          'pcre')
            use_spack_dep('harfbuzz')

        if version >= Version('5.7'):
            use_spack_dep('double-conversion', 'doubleconversion')

        if version <= Version('5.7.1'):
            config_args.append('-no-openvg')
        else:
            # FIXME: those could work for other versions
            use_spack_dep('libpng')
            use_spack_dep('jpeg', 'libjpeg')
            use_spack_dep('zlib')

        if '@:5.5' in spec:
            config_args.extend([
                # NIS is deprecated in more recent glibc,
                # but qt-5.6.3 does not recognize this option
                '-no-nis',
            ])

        # COMPONENTS

        if '~examples' in spec:
            config_args.extend(['-nomake', 'examples'])

        if '~tools' in spec:
            config_args.extend(['-nomake', 'tools'])

        if '+dbus' in spec:
            dbus = spec['dbus'].prefix
            config_args.append('-dbus-linked')
            config_args.append('-I%s/dbus-1.0/include' % dbus.lib)
            config_args.append('-I%s/dbus-1.0' % dbus.include)
            config_args.append('-L%s' % dbus.lib)
        else:
            config_args.append('-no-dbus')

        if MACOS_VERSION:
            config_args.append('-{0}framework'.format(
                '' if '+framework' in spec else 'no-'))

        (_, qtplat) = self.get_mkspec()
        if qtplat is not None:
            config_args.extend(['-platform', qtplat])

        return config_args

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
            '-xmlpatterns',
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

        use_spack_dep = self._dep_appender_factory(config_args)

        if MACOS_VERSION:
            if version < Version('5.9'):
                config_args.append('-no-xcb-xlib')
            if version < Version('5.12'):
                config_args.append('-no-xinput2')
            if spec.satisfies('@5.9'):
                # Errors on bluetooth even when bluetooth is disabled...
                # at least on apple-clang%12
                config_args.extend(['-skip', 'connectivity'])
        elif version < Version('5.15') and '+gui' in spec:
            # Linux-only QT5 dependencies
            config_args.append('-system-xcb')
            if '+opengl' in spec:
                config_args.append('-I{0}/include'.format(spec['libx11'].prefix))
                config_args.append('-I{0}/include'.format(spec['xproto'].prefix))

        # If the version of glibc is new enough Qt will configure features that
        # may not be supported by the kernel version on the system. This will
        # cause errors like:
        #   error while loading shared libraries: libQt5Core.so.5: cannot open
        #   shared object file: No such file or directory
        # Test the kernel version and disable features that Qt detects in glibc
        # but that are not supported in the kernel as determined by information
        # in: qtbase/src/corelib/global/minimum-linux_p.h.
        if LINUX_VERSION and version >= Version('5.10'):
            if LINUX_VERSION < Version('3.16'):
                config_args.append('-no-feature-renameat2')
            if LINUX_VERSION < Version('3.17'):
                config_args.append('-no-feature-getentropy')

        if '~webkit' in spec:
            config_args.extend([
                '-skip',
                'webengine' if version >= Version('5.6') else 'qtwebkit',
            ])

        if spec.satisfies('@5.7'):
            config_args.extend(['-skip', 'virtualkeyboard'])

        if version >= Version('5.8'):
            # relies on a system installed wayland, i.e. no spack package yet
            # https://wayland.freedesktop.org/ubuntu16.04.html
            # https://wiki.qt.io/QtWayland
            config_args.extend(['-skip', 'wayland'])

        if '~opengl' in spec:
            config_args.extend(['-skip', 'multimedia'])
            config_args.extend(['-skip', 'qt3d'])

            if version >= Version('5.10'):
                config_args.extend(['-skip', 'webglplugin'])

            if version >= Version('5.14'):
                config_args.extend(['-skip', 'qtquick3d'])

            if version >= Version('5.15'):
                config_args.extend(['-skip', 'qtlocation'])

        else:
            # v5.0: qt3d uses internal-only libassimp
            # v5.5: external-only libassimp
            # v5.6: either internal or external libassimp via autodetection
            # v5.9: user-selectable internal-vs-external via -assimp
            # v5.14: additional qtquick3d module uses -assimp
            # v5.15: qtquick3d switched to the -quick3d-assimp option
            if version >= Version('5.9'):
                use_spack_dep('assimp')
            elif version >= Version('5.15'):
                use_spack_dep('assimp', 'quick3d-assimp')

        if MACOS_VERSION and '+opengl' in spec:
            # These options are only valid if 'multimedia' is enabled, i.e.
            # +opengl is selected. Force them to be off on macOS, but let other
            # platforms decide for themselves.
            config_args.extend([
                '-no-pulseaudio',
                '-no-alsa',
            ])

        if spec.satisfies('platform=darwin target=aarch64:'):
            # https://www.qt.io/blog/qt-on-apple-silicon
            # Not currently working for qt@5
            config_args.extend(['-device-option',
                                'QMAKE_APPLE_DEVICE_ARCHS=arm64'])

        configure(*config_args)

    def build(self, spec, prefix):
        make()

    def install(self, spec, prefix):
        make("install")

    # Documentation generation requires the doc tools to be installed.
    # @when @run_after currently seems to ignore the 'when' restriction.
    @run_after('install')
    def install_docs(self):
        if '+doc' in self.spec:
            make('docs')
            make('install_docs')
