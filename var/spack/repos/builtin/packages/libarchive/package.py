# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libarchive(AutotoolsPackage):
    """libarchive: C library and command-line tools for reading and
       writing tar, cpio, zip, ISO, and other archive formats."""

    homepage = "http://www.libarchive.org"
    url      = "http://www.libarchive.org/downloads/libarchive-3.1.2.tar.gz"

    version('3.3.2', '4583bd6b2ebf7e0e8963d90879eb1b27')
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
