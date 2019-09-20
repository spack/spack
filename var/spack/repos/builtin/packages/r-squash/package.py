# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSquash(RPackage):
    """Color-Based Plots for Multivariate Visualization"""

    homepage = "https://cloud.r-project.org/package=squash"
    url      = "https://cloud.r-project.org/src/contrib/squash_1.0.8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/squash"

    version('1.0.8', '50d5743d306fa11cfa1a3c4daa75e508')
    version('1.0.7', '4ac381b17d4d7b77bdaa6f824fbb03ab')
