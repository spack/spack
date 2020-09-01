# Copyright 2013-2020 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Lcms2(AutotoolsPackage):
    """Little CMS intends to be an OPEN SOURCE small-footprint color
    management engine, with special focus on accuracy and performance.
    It uses the International Color Consortium standard (ICC), which
    is the modern standard when regarding to color management. """

    homepage = "https://github.com/ArtifexSoftware/thirdparty-lcms2"
    url      = "https://github.com/ArtifexSoftware/thirdparty-lcms2/archive/lcms2.10.tar.gz"

    version('2.10', sha256='2afb30f7546e8a3f91e6caa1a920fc6bb104e6f8351b7a114dd99603938d8f28')
    version('2.9',  sha256='a84d5b8c6fb0ef4d2583b5a45cb100a5e2e9c78ad7428cbe5808b3cc17d758be')
    version('2.8',  sha256='9c4a68e2c1504e411a59e08f3b0ef399dd00447356bae92fedb31f28a3a4cb97')
