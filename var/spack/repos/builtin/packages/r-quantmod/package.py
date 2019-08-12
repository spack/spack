# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RQuantmod(RPackage):
    """Specify, build, trade, and analyse quantitative financial trading
    strategies."""

    homepage = "http://www.quantmod.com/"
    url      = "https://cran.r-project.org/src/contrib/quantmod_0.4-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/quantmod"

    version('0.4-10', 'e4119c673567801eee16dcbbd0265de8')
    version('0.4-5', 'cab3c409e4de3df98a20f1ded60f3631')

    depends_on('r-xts', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-ttr', type=('build', 'run'))
    depends_on('r-curl', type=('build', 'run'))
