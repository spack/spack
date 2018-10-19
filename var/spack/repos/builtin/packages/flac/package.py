# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Flac(AutotoolsPackage):
    """Encoder/decoder for the Free Lossless Audio Codec"""

    homepage = "https://xiph.org/flac/index.html"
    url      = "http://downloads.xiph.org/releases/flac/flac-1.3.2.tar.xz"

    version('1.3.2', '454f1bfa3f93cc708098d7890d0499bd')
    version('1.3.1', 'b9922c9a0378c88d3e901b234f852698')
    version('1.3.0', '13b5c214cee8373464d3d65dee362cdd')

    depends_on('libvorbis')
    depends_on('id3lib')
