# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPosterior(RPackage):
    """Tools for Working with Posterior Distributions.

    Provides useful tools for both users and developers of packages for
    fitting Bayesian models or working with output from Bayesian models. The
    primary goals of the package are to: (a) Efficiently convert between many
    different useful formats of draws (samples) from posterior or prior
    distributions. (b) Provide consistent methods for operations commonly
    performed on draws, for example, subsetting, binding, or mutating draws.
    (c) Provide various summaries of draws in convenient formats. (d) Provide
    lightweight implementations of state of the art posterior inference
    diagnostics. References: Vehtari et al. (2021) <doi:10.1214/20-BA1221>."""

    cran = "posterior"

    version("1.3.1", sha256="7000780290a24be86dbc406dd4338aec622d8dee1e471b68b55abb4872934d7a")
    version("1.2.1", sha256="b757e06885a1f21e7ad8f5a3feaecbe0a71ae8d766e4aec4c3aa2183a810afe1")
    version("1.2.0", sha256="2ba01711a98448acc939cf506d22e8ee4cf680cdcea873226671fa8ae6934386")
    version("1.1.0", sha256="eff6262dbcc1bf18337f535b0c75ba2fe360322e8b170c466e24ed3ee76cf4d2")

    depends_on("r@3.2.0:", type=("build", "run"))
    depends_on("r-abind", type=("build", "run"))
    depends_on("r-checkmate", type=("build", "run"))
    depends_on("r-rlang@0.4.7:", type=("build", "run"))
    depends_on("r-tibble@3.0.0:", type=("build", "run"))
    depends_on("r-vctrs", type=("build", "run"))
    depends_on("r-tensora", type=("build", "run"))
    depends_on("r-pillar", type=("build", "run"))
    depends_on("r-distributional", type=("build", "run"))
    depends_on("r-matrixstats", type=("build", "run"))
