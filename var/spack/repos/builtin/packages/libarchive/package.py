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


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "http://www.libarchive.org"
    url      = "http://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    version('3.2.1', 'afa257047d1941a565216edbf0171e72')
    version('3.1.2', 'efad5a503f66329bb9d2f4308b5de98a')
    version('3.1.1', '1f3d883daf7161a0065e42a15bbf168f')
    version('3.1.0', '095a287bb1fd687ab50c85955692bf3a')

    depends_on('zlib')
    depends_on('bzip2')
    depends_on('lzma')
    depends_on('lz4')
    depends_on('xz')
    depends_on('lzo')
    depends_on('nettle')
    depends_on('openssl')
    depends_on('libxml2')
    depends_on('expat')

    # NOTE: `make check` is known to fail with the Intel compilers
    # The build test suite cannot be built with Intel
