# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Jline3(MavenPackage):
    """JLine is a Java library for handling console input."""

    homepage = "https://github.com/jline/jline3/"
    url      = "https://github.com/jline/jline3/archive/jline-parent-3.16.0.tar.gz"

    version('3.19.0', sha256='bbcf5fb07452af35784a606d71ac5e93c04e0a8a558007955e17577ea3466430')
    version('3.18.0', sha256='cf26cf08b7cb3228fcaa1c5b6113078d0163ecc51c21e636fbf990e8ae38c51b')
    version('3.17.1', sha256='ceeecbf999128342db5a6e3434e0b7eb6c228d11a1d363b52dfb290e7dd3a9c7')
    version('3.17.0', sha256='c9c6580bc50563b6c82bcc00dcafe19d75098b9d85027a0964dec289fe92273b')
    version('3.16.0', sha256='d2de8dfe55a55e20752aeb082a75192bf835baaab75f257d3fab90ce350fdbcb')
    version('3.15.0', sha256='3953c22efad2d525f1d1fbf8f02baa302da21c18f3f60a19ee216e819fab9ac1')
    version('3.14.1', sha256='9b1bdb48af772eb60a010544bc28a6cca565d2856ababe5684e0938ca519335b')
    version('3.14.0', sha256='8e0bee3d2f2b734723a3cef441b6a5e2b6c11193f80030a7119f94a43a964bbf')
    version('3.13.3', sha256='ebba1b156820390835fb56e12d6ca7dad77fe85eee1f5f761019ec87ca32da86')
