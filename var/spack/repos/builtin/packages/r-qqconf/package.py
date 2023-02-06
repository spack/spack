# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
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

    version("1.3.0", sha256="1c42ab81403568f3ad53217cc85190dad7c2fae957bfd0f0f30d57be0a065087")
    version("1.2.3", sha256="9b5b6042ea8e52e6e049807c0b5e3bfd534b624bd257be769de69cf505fece62")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r@4.0.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-mass@7.3-50:", type=("build", "run"))
    depends_on("r-robustbase@0.93-4:", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("fftw@3.1.2:")
    depends_on("r-dplyr@1.0.0:", type=("build", "run"))
    depends_on("r-dplyr", when="@:1.2.3")
    depends_on("r-magrittr@1.5:", type=("build", "run"))
    depends_on("r-magrittr", when="@:1.2.3")
    depends_on("r-rlang@0.4.9:", type=("build", "run"))
    depends_on("r-rlang", when="@:1.2.3")
