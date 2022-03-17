# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *
import os


class Qt6base(CMakePackage):
    """Qt Base (Core, Gui, Widgets, Network, ...)"""

    homepage = "https://www.qt.io"
    url      = "https://github.com/qt/qtbase/archive/refs/tags/v6.2.3.tar.gz"

    maintainers = ['wdconinc', 'sethrj']

    version('6.2.3', sha256='2dd095fa82bff9e0feb7a9004c1b2fb910f79ecc6111aa64637c95a02b7a8abb')

    generator = 'Ninja'

    # Changing default to Release for typical use in HPC contexts
    variant('build_type',
            default='Release',
            values=("Release", "Debug", "RelWithDebInfo", "MinSizeRel"),
            description='CMake build type')

    variant('accessibility', default=True, description='Build with accessibility support.')
    variant('dbus', default=False, description='Build with D-Bus support.')
    variant('examples', default=False, description='Build examples.')
    variant('framework', default=False, description='Build as a macOS Framework package.')
    variant('gtk', default=False, description='Build with gtkplus.')
    variant('gui', default=True, description='Build the Qt GUI module and dependencies.')
    variant('opengl', default=False, description='Build with OpenGL support.')
    variant('shared', default=True, description='Build shared libraries.')
    variant('sql', default=True, description='Build with SQL support.')
    variant('ssl', default=True, description='Build with OpenSSL support.')
    variant('tests', default=False, description='Build tests.')
    variant('widgets', default=True, description='Build with widgets.')

    depends_on('cmake@3.16:', type='build')
    depends_on('ninja', type='build')
    depends_on("pkgconfig", type='build')
    depends_on("python", type='build')

    # Dependencies, then variant- and version-specific dependencies
    depends_on('at-spi2-core', when='+accessibility')
    depends_on('dbus', when='+dbus')
    depends_on('double-conversion')
    depends_on('fontconfig')
    depends_on("freetype")
    depends_on('gl', when='+opengl')
    depends_on("harfbuzz")
    depends_on("icu4c")
    depends_on("jpeg")
    depends_on('libdrm')
    depends_on('libjpeg')
    depends_on("libmng")
    depends_on('libproxy')
    depends_on("libtiff")
    depends_on('libxkbcommon')
    depends_on("libxml2")
    depends_on('libxrender')
    depends_on('openssl', when='+ssl')
    depends_on('pcre2+multibyte')
    depends_on("sqlite", when='+sql')
    depends_on("zlib")
    depends_on("zstd")

    def patch(self):
        import shutil
        vendor_dir = join_path(self.stage.source_path, 'src/3rdparty')
        vendor_deps_to_keep = [
            'blake2', 'easing', 'forkfd', 'freebsd',
            'icc', 'md4', 'md4c', 'md5', 'rfc6234',
            'sha1', 'sha3', 'tinycbor', 'VulkanMemoryAllocator',
        ]
        with working_dir(vendor_dir):
            for dep in os.listdir():
                if os.path.isdir(dep):
                    if dep not in vendor_deps_to_keep:
                        shutil.rmtree(dep)

    def cmake_args(self):
        args = [
            self.define('FEATURE_optimize_size',
                self.spec.satisfies('build_type=MinSizeRel')), 
            self.define_from_variant('FEATURE_accessibility', 'accessibility'),
            self.define_from_variant('FEATURE_dbus', 'dbus'),
            self.define('INPUT_dbus', 'linked'),
            self.define_from_variant('FEATURE_framework', 'framework'),
            self.define_from_variant('FEATURE_gui', 'gui'),
            self.define_from_variant('FEATURE_ssl', 'ssl'),
            self.define('INPUT_openssl', 'linked'),
            self.define_from_variant('FEATURE_widgets', 'widgets'),
            self.define_from_variant('QT_BUILD_EXAMPLES', 'examples'),
            self.define_from_variant('QT_BUILD_TESTS', 'tests'),
            self.define_from_variant('BUILD_SHARED_LIBS', 'shared'),
            self.define('FEATURE_system_doubleconversion', True),
            self.define('FEATURE_system_freetype', True),
            self.define('FEATURE_system_harfbuzz', True),
            self.define('FEATURE_system_jpeg', True),
            self.define('FEATURE_system_libb2', False),
            self.define_from_variant('INPUT_opengl', 'opengl'),
            self.define('FEATURE_system_pcre2', True),
            self.define('FEATURE_system_png', True),
            self.define('FEATURE_system_proxies', True),
            self.define_from_variant('FEATURE_sql', 'sql'), 
            self.define('FEATURE_system_sqlite', True),
            self.define('FEATURE_system_textmarkdownreader', False),
            self.define('FEATURE_system_zlib', True),
        ]
        return args
