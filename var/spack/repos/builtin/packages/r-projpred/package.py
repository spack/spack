# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RProjpred(RPackage):
    """Projection Predictive Feature Selection.

    Performs projection predictive feature selection for generalized linear
    models and generalized linear and additive multilevel models (see,
    Piironen, Paasiniemi and Vehtari, 2020,
    <https://projecteuclid.org/euclid.ejs/1589335310>, Catalina, Burkner and
    Vehtari, 2020, <arXiv:2010.06994>). The package is compatible with the
    'rstanarm' and 'brms' packages, but other reference models can also be
    used. See the package vignette for more information and examples."""

    cran = "projpred"

    version("2.5.0", sha256="b6ec123f5bf573d14cbd5431e3fbdee3215d71d3e263fcbec72bee5930044e39")
    version("2.2.1", sha256="6825ace07d1e580d5916bcd6bfd163460ae9008926f464e00deb7f2395cc72ad")
    version("2.1.2", sha256="a88a651e533c118aad0e8c2c905cfcf688d9c419ed195896036b8f6667b5cfb0")
    version("2.0.2", sha256="af0a9fb53f706090fe81b6381b27b0b6bd3f7ae1e1e44b0ada6f40972b09a55b")

    depends_on("r@3.5.0:", type=("build", "run"))
    depends_on("r-loo@2.0.0:", type=("build", "run"))
    depends_on("r-rstantools@2.0.0:", type=("build", "run"))
    depends_on("r-lme4", type=("build", "run"))
    depends_on("r-lme4@1.1-28:", when="@2.5.0:", type=("build", "run"))
    depends_on("r-mvtnorm", when="@2.1.2:", type=("build", "run"))
    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-rcpp", type=("build", "run"))
    depends_on("r-abind", when="@2.5.0:", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"))
    depends_on("r-gamm4", type=("build", "run"))
    depends_on("r-mclogit", when="@2.5.0:", type=("build", "run"))
    depends_on("r-nnet", when="@2.5.0:", type=("build", "run"))
    depends_on("r-ucminf", when="@2.5.0:", type=("build", "run"))
    depends_on("r-ordinal", when="@2.5.0:", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-rcpparmadillo", type=("build", "run"))

    depends_on("r-optimx", when="@:2.0.2", type=("build", "run"))
    depends_on("r-rngtools@1.2.4:", when="@:2.0.2", type=("build", "run"))
    depends_on("r-tidyverse", when="@:2.0.2", type=("build", "run"))
    depends_on("r-dplyr", when="@:2.2.1", type=("build", "run"))
    depends_on("r-magrittr", when="@:2.2.1", type=("build", "run"))
    depends_on("r-rlang", when="@2.1.2:2.2.1", type=("build", "run"))
