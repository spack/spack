# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Ffmpeg(AutotoolsPackage):
    """FFmpeg is a complete, cross-platform solution to record,
    convert and stream audio and video."""

    homepage = "https://ffmpeg.org"
    url      = "http://ffmpeg.org/releases/ffmpeg-3.2.4.tar.bz2"

    version('3.2.4', 'd3ebaacfa36c6e8145373785824265b4')
    version('4.2', '41b4ade83439fafe635001127f1056d4')

    variant('shared', default=True,
            description='build shared libraries')
    variant('x264', default=True,
            description='enable x264 encoder')

    depends_on('yasm@1.2.0:')
    depends_on('x264', when='@4.2: +x264')


    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+shared' in spec:
            config_args.append('--enable-shared')

        if '+x264' in spec and self.version >= Version('4.2'):
            config_args.append('--enable-libx264')
            config_args.append('--enable-gpl')
        return config_args
