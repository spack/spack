# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Eve(CMakePackage):
    """Expressive Velocity Engine - SIMD in C++ Goes Brrrr"""

    homepage = "https://jfalcou.github.io/eve/"
    url      = "https://github.com/jfalcou/eve/archive/refs/tags/v2021.10.0.tar.gz"
    maintainers = ['jfalcou']
    git = 'https://github.com/jfalcou/eve.git'

    version('develop', branch='develop')
    version('2021.10.0', sha256='580c40a8244039a700b93ea49fb0affc1c8d3c100eb6dc66368e101753f51e5c')
