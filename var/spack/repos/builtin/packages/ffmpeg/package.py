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

    version('3.2.4',   'd3ebaacfa36c6e8145373785824265b4')

    variant('shared', default=True,
            description='build shared libraries')

    depends_on('yasm@1.2.0:')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+shared' in spec:
            config_args.append('--enable-shared')

        return config_args
