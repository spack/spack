# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RQqconf(RPackage):
    """Creates Simultaneous Testing Bands for QQ-Plots.

    Provides functionality for creating Quantile-Quantile (QQ) and
    Probability-Probability (PP) plots with simultaneous testing bands to asses
    significance of sample deviation from a reference distribution."""

    cran = "qqconf"

    version("1.2.3", sha256="9b5b6042ea8e52e6e049807c0b5e3bfd534b624bd257be769de69cf505fece62")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-dplyr@1.0.0:", type=("build", "run"))
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-rlang@0.4.9:", type=("build", "run"))
    depends_on("r-mass@7.3-50:", type=("build", "run"))
    depends_on("r-robustbase@0.93-4:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("fftw@3.1.2:")
