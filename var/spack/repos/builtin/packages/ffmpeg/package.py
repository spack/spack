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

    version('4.2', '41b4ade83439fafe635001127f1056d4')
    version('4.1.1',   '4a64e3cb3915a3bf71b8b60795904800')
    version('4.1',   'b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4', 'd3ebaacfa36c6e8145373785824265b4')

    variant('shared', default=True,
            description='build shared libraries')
    variant('x264', default=True,
            description='enable x264 encoder')
    variant('aom', default=False,
            description='build Alliance for Open Media libraries')

    depends_on('yasm@1.2.0:')
    depends_on('x264', when='@4.2: +x264')
    depends_on('aom', when='+aom')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+shared' in spec:
            config_args.append('--enable-shared')

        if '+x264' in spec and self.version >= Version('4.2'):
            config_args.append('--enable-libx264')
            config_args.append('--enable-gpl')
        if '+aom' in spec:
            config_args.append('--enable-libaom')
        else:
            config_args.append('--disable-libaom')

        return config_args
