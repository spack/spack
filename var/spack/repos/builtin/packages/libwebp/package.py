# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Libwebp(CMakePackage):
    """
    WebP is a modern image format that provides superior lossless and lossy
    compression for images on the web. Using WebP, webmasters and web
    developers can create smaller, richer images that make the web faster.
    """

    homepage = "https://developers.google.com/speed/webp/"
    url      = "https://github.com/webmproject/libwebp/archive/v1.0.3.tar.gz"

    version('1.0.3',     sha256='082d114bcb18a0e2aafc3148d43367c39304f86bf18ba0b2e766447e111a4a91')
