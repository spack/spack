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
import glob
from spack import *


class Rhash(MakefilePackage):
    """RHash is a console utility for computing and verifying hash sums of
    files. It supports CRC32, MD4, MD5, SHA1, SHA256, SHA512, SHA3, Tiger,
    TTH, Torrent BTIH, AICH, ED2K, GOST R 34.11-94, RIPEMD-160, HAS-160,
    EDON-R 256/512, WHIRLPOOL and SNEFRU hash sums."""

    homepage = "https://sourceforge.net/projects/rhash/"
    url      = "https://github.com/rhash/RHash/archive/v1.3.5.tar.gz"

    version('1.3.5', 'f586644019c10c83c6b6835de4b99e74')

    # For macOS build instructions, see:
    # https://github.com/Homebrew/homebrew-core/blob/master/Formula/rhash.rb

    def build(self, spec, prefix):
        # Doesn't build shared libraries by default
        make()

        if spec.satisfies('platform=darwin'):
            make('-C', 'librhash', 'dylib')
        else:
            make('lib-shared')

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

    def install(self, spec, prefix):
        # Some things are installed to $(DESTDIR)$(PREFIX) while other things
        # are installed to $DESTDIR/etc.
        make('install', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
        make('install-lib-static', 'DESTDIR={0}'.format(prefix), 'PREFIX=')

        if spec.satisfies('platform=darwin'):
            libs = glob.glob('librhash/*.dylib')
            for lib in libs:
                install(lib, prefix.lib)
        else:
            make('install-lib-shared', 'DESTDIR={0}'.format(prefix), 'PREFIX=')
