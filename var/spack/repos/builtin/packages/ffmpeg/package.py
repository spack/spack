# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url      = "http://ffmpeg.org/releases/ffmpeg-4.1.1.tar.bz2"

    version('4.1.1',   '4a64e3cb3915a3bf71b8b60795904800')
    version('4.1',   'b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4', 'd3ebaacfa36c6e8145373785824265b4')

    variant('shared', default=True,
            description='build shared libraries')

    variant('aom', default=False,
            description='build Alliance for Open Media libraries')

    variant('x264', default=False,
            description='Enable libx264 codec support")

    depends_on('yasm@1.2.0:')
    depends_on('aom', when='+aom')
    depends_on('libx264', when="+x264")

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        config_args.extend(self.enable_or_disable('shared'))
        config_args.extend(self.enable_or_disable('aom'))

        if '+x264' in spec:
            config_args.extend(['--enable-gpl',
                                '--enable-libx264',
                                '--enable-encoder=libx264'])

        return config_args
