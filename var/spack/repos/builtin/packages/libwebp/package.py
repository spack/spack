# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class Libwebp(AutotoolsPackage):
    """WebP is a modern image format that provides superior lossless and lossy
    compression for images on the web. Using WebP, webmasters and web
    developers can create smaller, richer images that make the web faster."""

    homepage = "https://developers.google.com/speed/webp/"
    url      = "https://storage.googleapis.com/downloads.webmproject.org/releases/webp/libwebp-1.0.3.tar.gz"

    version('1.2.0', sha256='2fc8bbde9f97f2ab403c0224fb9ca62b2e6852cbc519e91ceaa7c153ffd88a0c')
    version('1.0.3', sha256='e20a07865c8697bba00aebccc6f54912d6bc333bb4d604e6b07491c1a226b34f')

    variant('libwebpmux', default=False, description='Build libwebpmux')
    variant('libwebpdemux', default=False, description='Build libwebpdemux')
    variant('libwebpdecoder', default=False, description='Build libwebpdecoder')
    variant('libwebpextras', default=False, description='Build libwebpextras')
    variant('gif', default=False, description='GIF support')
    variant('jpeg', default=False, description='JPEG support')
    variant('png', default=False, description='PNG support')
    variant('tiff', default=False, description='TIFF support')

    depends_on('automake', type='build')
    depends_on('autoconf', type='build')
    depends_on('libtool', type='build')
    depends_on('m4', type='build')
    depends_on('giflib', when='+gif')
    depends_on('jpeg', when='+jpeg')
    depends_on('libpng', when='+png')
    depends_on('libtiff', when='+tiff')

    def configure_args(self):
        # TODO: add variants and dependencies for these
        args = [
            '--disable-gl',
            '--disable-sdl',
            '--disable-wic',
        ]

        args += self.enable_or_disable('gif')
        args += self.enable_or_disable('jpeg')
        args += self.enable_or_disable('png')
        args += self.enable_or_disable('tiff')
        args += self.enable_or_disable('libwebpmux')
        args += self.enable_or_disable('libwebpdemux')
        args += self.enable_or_disable('libwebpdecoder')
        args += self.enable_or_disable('libwebpextras')

        return args
