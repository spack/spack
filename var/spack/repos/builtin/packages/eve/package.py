# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class Eve(CMakePackage):
    """Expressive Velocity Engine - SIMD in C++ Goes Brrrr"""

    homepage = "https://jfalcou.github.io/eve/html/index.html"
    url      = "https://github.com/jfalcou/eve/archive/refs/tags/v2022.03.0.tar.gz"
    maintainers = ['jfalcou']
    git = 'https://github.com/jfalcou/eve.git'

    version('main', branch='main')
    version('2022.03.0', sha256='8bf9faea516806e7dd468e778dcedc81c51f0b2c6a70b9c75987ce12bb759911')
    version('2021.10.0', sha256='580c40a8244039a700b93ea49fb0affc1c8d3c100eb6dc66368e101753f51e5c')
