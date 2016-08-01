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


class Libarchive(Package):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""
    homepage = "http://www.libarchive.org"
    url      = "http://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    version('3.2.1', 'afa257047d1941a565216edbf0171e72')
    version('3.1.2', 'efad5a503f66329bb9d2f4308b5de98a')
    version('3.1.1', '1f3d883daf7161a0065e42a15bbf168f')
    version('3.1.0', '095a287bb1fd687ab50c85955692bf3a')

    variant('zlib',    default=True, description='Build support for gzip through zlib')
    variant('bzip2',   default=True, description='Build support for bzip2 through bz2lib')
    variant('lzma',    default=True, description='Build support for lzma through lzmadec')
    variant('lz4',     default=True, description='Build support for lz4 through liblz4')
    variant('xz',      default=True, description='Build support for xz through lzma')
    variant('lzo',     default=True, description='Build support for lzop through liblzo2')
    variant('nettle',  default=True, description='Build with crypto support from Nettle')
    variant('openssl', default=True, description='Build support for mtree and xar hashes through openssl')
    variant('libxml2', default=True, description='Build support for xar through libxml2')
    variant('expat',   default=True, description='Build support for xar through expat')

    depends_on('zlib',    when='+zlib')
    depends_on('bzip2',   when='+bzip2')
    depends_on('lzma',    when='+lzma')
    depends_on('lz4',     when='+lz4')
    depends_on('xz',      when='+xz')
    depends_on('lzo',     when='+lzo')
    depends_on('nettle',  when='+nettle')
    depends_on('openssl', when='+openssl')
    depends_on('libxml2', when='+libxml2')
    depends_on('expat',   when='+expat')

    def install(self, spec, prefix):
        def variant_to_bool(variant):
            return 'with' if variant in spec else 'without'

        config_args = [
            '--prefix={0}'.format(prefix),
            '--{0}-zlib'.format(variant_to_bool('+zlib')),
            '--{0}-bz2lib'.format(variant_to_bool('+bzip2')),
            '--{0}-lzmadec'.format(variant_to_bool('+lzma')),
            '--{0}-lz4'.format(variant_to_bool('+lz4')),
            '--{0}-lzma'.format(variant_to_bool('+xz')),
            '--{0}-lzo2'.format(variant_to_bool('+lzo')),
            '--{0}-nettle'.format(variant_to_bool('+nettle')),
            '--{0}-openssl'.format(variant_to_bool('+openssl')),
            '--{0}-xml2'.format(variant_to_bool('+libxml2')),
            '--{0}-expat'.format(variant_to_bool('+expat'))
        ]

        configure(*config_args)

        make()
        # make('check')  # cannot build test suite with Intel compilers
        make('install')
