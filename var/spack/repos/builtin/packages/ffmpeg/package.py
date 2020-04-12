# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url      = "http://ffmpeg.org/releases/ffmpeg-4.1.1.tar.bz2"

    version('4.2.2', sha256='b620d187c26f76ca19e74210a0336c3b8380b97730df5cdf45f3e69e89000e5c')
    version('4.1.1', sha256='0cb40e3b8acaccd0ecb38aa863f66f0c6e02406246556c2992f67bf650fab058')
    version('4.1',   sha256='b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4', sha256='c0fa3593a2e9e96ace3c1757900094437ad96d1d6ca19f057c378b5f394496a4')

    # Licensing
    variant('gpl', default=True,
            description='allow use of GPL code, the resulting libs '
            'and binaries will be under GPL')
    variant('version3', default=True,
            description='upgrade (L)GPL to version 3')
    variant('nonfree', default=False,
            description='allow use of nonfree code, the resulting libs '
            'and binaries will be unredistributable')

    # NOTE: The libopencv option creates a circular dependency.
    # NOTE: There are more possible variants that would require additional
    # spack packages.

    # meta variants: These will toggle several settings
    variant('X', default=False, description='X11 support')
    variant('drawtext', default=False, description='drawtext filter')

    # options
    variant('bzlib', default=True, description='bzip2 support')
    variant('libaom', default=False, description='AV1 video encoding/decoding')
    variant('libmp3lame', default=False, description='MP3 encoding')
    variant('libopenjpeg', default=False, description='JPEG 2000 de/encoding')
    variant('libopus', default=False, description='Opus de/encoding')
    variant('libsnappy', default=False,
            description='Snappy compression, needed for hap encoding')
    variant('libspeex', default=False, description='Speex de/encoding')
    variant('libssh', default=False, description='SFTP protocol')
    variant('libvorbis', default=False, description='Vorbis en/decoding')
    variant('libwebp', default=False, description='WebP encoding via libwebp')
    # TODO: There is an issue with the spack headers property in the libxml2
    # package recipe. Comment out the libxml2 variant until that is resolved.
    # variant('libxml2', default=False,
    #         description='XML parsing, needed for dash demuxing support')
    variant('libzmq', default=False, description='message passing via libzmq')
    variant('lzma', default=True, description='lzma support')
    variant('openssl', default=False, description='needed for https support')
    variant('sdl2', default=True, description='sdl2 support')
    variant('shared', default=True, description='build shared libraries')

    depends_on('alsa-lib')
    depends_on('libiconv')
    depends_on('yasm@1.2.0:')
    depends_on('zlib')

    depends_on('aom', when='+libaom')
    depends_on('bzip2', when='+bzlib')
    depends_on('fontconfig', when='+drawtext')
    depends_on('freetype', when='+drawtext')
    depends_on('fribidi', when='+drawtext')
    depends_on('lame', when='+libmp3lame')
    depends_on('libssh', when='+libssh')
    depends_on('libvorbis', when='+libvorbis')
    depends_on('libwebp', when='+libwebp')
    # TODO: enable libxml2 when libxml2 header issue is resolved
    # depends_on('libxml2', when='+libxml2')
    depends_on('libxv', when='+X')
    depends_on('libzmq', when='+libzmq')
    depends_on('openjpeg', when='+libopenjpeg')
    depends_on('openssl', when='+openssl')
    depends_on('opus', when='+libopus')
    depends_on('sdl2', when='+sdl2')
    depends_on('snappy', when='+libsnappy')
    depends_on('speex', when='+libspeex')
    depends_on('xz', when='+lzma')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+X' in spec:
            config_args.extend([
                '--enable-libxcb',
                '--enable-libxcb-shape',
                '--enable-libxcb-shm',
                '--enable-libxcb-xfixes',
                '--enable-xlib',
            ])
        else:
            config_args.extend([
                '--disable-libxcb',
                '--disable-libxcb-shape',
                '--disable-libxcb-shm',
                '--disable-libxcb-xfixes',
                '--disable-xlib',
            ])

        if '+drawtext' in spec:
            config_args.extend([
                '--enable-libfontconfig',
                '--enable-libfreetype',
                '--enable-libfribidi',
            ])
        else:
            config_args.extend([
                '--disable-libfontconfig',
                '--disable-libfreetype',
                '--disable-libfribidi',
            ])
        for variant in [
            'bzlib',
            'libaom',
            'libmp3lame',
            'libopenjpeg',
            'libopus',
            'libsnappy',
            'libspeex',
            'libssh',
            'libvorbis',
            'libwebp',
            # TODO: enable when libxml2 header issue is resolved
            # 'libxml2',
            'libzmq',
            'lzma',
            'openssl',
            'sdl2',
            'shared',
        ]:
            config_args += self.enable_or_disable(variant)

        return config_args
