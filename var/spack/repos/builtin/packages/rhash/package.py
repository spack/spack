# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

import os


class Rhash(MakefilePackage):
    """RHash is a console utility for computing and verifying hash sums of
    files. It supports CRC32, MD4, MD5, SHA1, SHA256, SHA512, SHA3, Tiger,
    TTH, Torrent BTIH, AICH, ED2K, GOST R 34.11-94, RIPEMD-160, HAS-160,
    EDON-R 256/512, WHIRLPOOL and SNEFRU hash sums."""

    homepage = "https://sourceforge.net/projects/rhash/"
    url      = "https://github.com/rhash/RHash/archive/v1.3.5.tar.gz"

    version('1.4.2', sha256='600d00f5f91ef04194d50903d3c79412099328c42f28ff43a0bdb777b00bec62')
    version('1.3.5', sha256='98e0688acae29e68c298ffbcdbb0f838864105f9b2bd8857980664435b1f1f2e')

    # configure: fix clang detection on macOS
    # Patch accepted and merged upstream, remove on next release
    patch('https://github.com/rhash/RHash/commit/4dc506066cf1727b021e6352535a8bb315c3f8dc.patch?full_index=1',
          when='@1.4.2', sha256='3fbfe4603d2ec5228fd198fc87ff3ee281e1f68d252c1afceaa15cba76e9b6b4')

    # For macOS build instructions, see:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/rhash.rb

    def configure(self, spec, prefix):
        set_executable('configure')
        configure_ = Executable('./configure')
        configure_('--prefix=')

    @when('@:1.4.1')
    def build(self, spec, prefix):
        # Doesn't build shared libraries by default
        make('PREFIX={0}'.format(prefix))

        if spec.satisfies('platform=darwin'):
            make('PREFIX={0}'.format(prefix), '-C', 'librhash', 'dylib')
        else:
            make('PREFIX={0}'.format(prefix), 'lib-shared')

    @when('@1.4.2:')
    def build(self, spec, prefix):
        self.configure(spec, prefix)
        make()

    def check(self):
        # Makefile has both `test` and `check` targets:
        #
        # * `test`  - used to test that the build is working properly
        # * `check` - used to check that the tarball is ready for upload
        #
        # Default implmentation is to run both `make test` and `make check`.
        # `test` passes, but `check` fails, so only run `test`.
        make('test')
        make('test-static-lib')

        if not self.spec.satisfies('platform=darwin'):
            make('test-shared')
            make('test-shared-lib')

    @when('@:1.4.1')
    def install(self, spec, prefix):
        # Some things are installed to $(DESTDIR)$(PREFIX) while other things
        # are installed to $DESTDIR/etc.
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
        make('install-lib-static', 'DESTDIR={0}'.format(prefix), 'PREFIX=')

        if spec.satisfies('platform=darwin'):
            install('librhash/*.dylib', prefix.lib)
        else:
            make('install-lib-shared', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
            os.symlink(join_path(prefix.lib, 'librhash.so.0'),
                       join_path(prefix.lib, 'librhash.so'))

    @when('@1.4.2:')
    def install(self, spec, prefix):
        make('install', 'DESTDIR={0}'.format(prefix))
        make('install-pkg-config', 'DESTDIR={0}'.format(prefix))
        make('install-lib-so-link', 'DESTDIR={0}'.format(prefix))
        make('install-lib-headers', 'DESTDIR={0}'.format(prefix))
