# Copyright 2013-2021 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Fping(AutotoolsPackage):
    """High performance ping tool."""

    homepage = "https://fping.org/"
    url      = "https://github.com/schweikert/fping/archive/v4.2.tar.gz"

    version('5.0', sha256='ed38c0b9b64686a05d1b3bc1d66066114a492e04e44eef1821d43b1263cd57b8')
    version('4.4', sha256='9f854b65a52dc7b1749d6743e35d0a6268179d1a724267339fc9a066b2b72d11')
    version('4.3', sha256='92040ae842f7b8942d5cf26d8f58702a8d84c40a1fd492b415bd01b622bf372d')
    version('4.2', sha256='49b0ac77fd67c1ed45c9587ffab0737a3bebcfa5968174329f418732dbf655d4')
    version('4.1', sha256='1da45b1d8c2d38b52bebd4f8b1617ddfae678e9f6436dafa6f62e97b8ecfc93c')
    version('4.0', sha256='8c9eac7aeadb5be0daa978cdac5f68ae44b749af0f643e8252b5e3dd4ce32e6a')

    depends_on('m4',       type='build')
    depends_on('autoconf', type='build')
    depends_on('automake', type='build')
    depends_on('libtool',  type='build')
