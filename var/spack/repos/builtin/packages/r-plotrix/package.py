# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPlotrix(RPackage):
    """Lots of plots, various labeling, axis and color scaling functions."""

    homepage = "https://cran.r-project.org/package=plotrix"
    url      = "https://cran.r-project.org/src/contrib/plotrix_3.6-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/plotrix"

    version('3.6-4', 'efe9b9b093d8903228a9b56c46d943fa')
    version('3.6-3', '23e3e022a13a596e9b77b40afcb4a2ef')
