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

    version('4.1.1',   sha256='0cb40e3b8acaccd0ecb38aa863f66f0c6e02406246556c2992f67bf650fab058')
    version('4.1',   sha256='b684fb43244a5c4caae652af9022ed5d85ce15210835bce054a33fb26033a1a5')
    version('3.2.4', sha256='c0fa3593a2e9e96ace3c1757900094437ad96d1d6ca19f057c378b5f394496a4')

    variant('shared', default=True,
            description='build shared libraries')

    variant('aom', default=False,
            description='build Alliance for Open Media libraries')

    depends_on('yasm@1.2.0:')
    depends_on('aom', when='+aom')

    def configure_args(self):
        spec = self.spec
        config_args = ['--enable-pic']

        if '+shared' in spec:
            config_args.append('--enable-shared')

        if '+aom' in spec:
            config_args.append('--enable-libaom')
        else:
            config_args.append('--disable-libaom')

        return config_args
