# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Squashfuse(AutotoolsPackage):
    """squashfuse - Mount SquashFS archives using FUSE"""

    homepage = "https://github.com/vasi/squashfuse"
    url      = "https://github.com/vasi/squashfuse/archive/refs/tags/0.1.104.tar.gz"
    git      = "https://github.com/vasi/squashfuse.git"

    maintainers = ['haampie']

    version('master', branch='master')
    version('0.1.104', sha256='9e6f4fb65bb3e5de60c8714bb7f5cbb08b5534f7915d6a4aeea008e1c669bd35')
    version('0.1.103', sha256='bba530fe435d8f9195a32c295147677c58b060e2c63d2d4204ed8a6c9621d0dd')

    variant('zlib', default=True, description='Enable zlib/gzip compression support')
    variant('lz4', default=True, description='Enable LZ4 compression support')
    variant('lzo', default=True, description='Enable LZO compression support')
    variant('xz', default=True, description='Enable xz compression support')
    variant('zstd', default=True, description='Enable Zstandard/zstd support')

    depends_on('libfuse@2.5:')
    depends_on('libfuse@:2.99', when='@:0.1.103')

    # Note: typically libfuse is external, but this implies that you have to make
    # pkg-config external too, because spack's pkg-config doesn't know how to
    # locate system pkg-config's fuse.pc/fuse3.pc
    depends_on('pkg-config', type='build')

    # compression libs
    depends_on('zlib', when='+zlib')
    depends_on('lz4', when='+lz4')
    depends_on('lzo', when='+lzo')
    depends_on('xz', when='+xz')
    depends_on('zstd', when='+zstd')

    # not all releases have a configure script
    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')

    def configure_args(self):
        args = ['--disable-demo']
        args += self.with_or_without('zlib', activation_value='prefix')
        args += self.with_or_without('lz4', activation_value='prefix')
        args += self.with_or_without('lzo', activation_value='prefix')
        args += self.with_or_without('xz', activation_value='prefix')
        args += self.with_or_without('zstd', activation_value='prefix')
        return args
