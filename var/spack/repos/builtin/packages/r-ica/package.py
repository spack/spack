# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RIca(RPackage):
    """Independent Component Analysis (ICA) using various algorithms: FastICA,
    Information-Maximization (Infomax), and Joint Approximate Diagonalization
    of Eigenmatrices (JADE)."""

    homepage = "https://cran.r-project.org/web/packages/ica/index.html"
    url      = "https://cran.r-project.org/src/contrib/ica_1.0-1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/ica"

    depends_on('r@3.4.0:3.4.9')
    version('1.0-1', '15c8d5afeec2804beec55dd14abc585d')
    version('1.0-0', '3ade2b3b00eb39c348d802f24d2afd1d')
