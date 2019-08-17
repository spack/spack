# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPackrat(RPackage):
    """Manage the R packages your project depends on in an isolated, portable,
    and reproducible way."""

    homepage = "https://github.com/rstudio/packrat/"
    url      = "https://cran.r-project.org/src/contrib/packrat_0.4.7-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/packrat"

    version('0.4.8-1', '14e82feba55fcda923396282fc490038')
    version('0.4.7-1', '80c2413269b292ade163a70ba5053e84')
