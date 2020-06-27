# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfs(MakefilePackage):
    """Squashfs - read only compressed filesystem"""

    homepage = 'http://squashfs.sourceforge.net'
    url      = 'https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz'

    # version      sha1
    version('4.4', sha256='a981b3f3f2054b5a2e658851a3c06a2460ad04a9a8a645e0afe063a63fdbb07e')
    version('4.3', sha256='0d605512437b1eb800b4736791559295ee5f60177e102e4d4ccd0ee241a5f3f6')
    version('4.2', sha256='d9e0195aa922dbb665ed322b9aaa96e04a476ee650f39bbeadb0d00b24022e96')
    version('4.1', sha256='3a870d065a25b3f5467bc6d9ed34340befab51a3f9e4b7e3792ea0ff4e06046a')
    version('4.0', sha256='18948edbe06bac2c4307eea99bfb962643e4b82e5b7edd541b4d743748e12e21')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
    depends_on('zlib')

    def build(self, spec, prefix):
        with working_dir('squashfs-tools'):
            make(parallel=False)

    def install(self, spec, prefix):
        with working_dir('squashfs-tools'):
            make('install', 'INSTALL_DIR=%s' % prefix.bin, parallel=False)
