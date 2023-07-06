# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RCompositions(RPackage):
    """Compositional Data Analysis.

    Provides functions for the consistent analysis of compositional  data (e.g.
    portions of substances) and positive numbers (e.g. concentrations)  in the
    way proposed by J. Aitchison and V. Pawlowsky-Glahn."""

    cran = "compositions"

    version("2.0-6", sha256="45d374ebfdcc2c9f6cc738d196caf83a2297ed2aefe2cc99007fcbeb78a61c34")
    version("2.0-4", sha256="7b9c7a3bf654fb02d9eb1b4a7566469b2f5232f3b2c1b324c02239fd31060faf")
    version("2.0-1", sha256="84a291308faf858e5a9d9570135c2da5e57b0887f407903485fa85d09da61a0f")
    version("1.40-2", sha256="110d71ae000561987cb73fc76cd953bd69d37562cb401ed3c36dca137d01b78a")

    depends_on("r@2.2.0:", type=("build", "run"))
    depends_on("r@3.6:", type=("build", "run"), when="@2.0-4:")

    depends_on("r-tensora", type=("build", "run"))
    depends_on("r-robustbase", type=("build", "run"))
    depends_on("r-bayesm", type=("build", "run"))
    depends_on("r-mass", type=("build", "run"), when="@2.0-1:")

    depends_on("r-energy", type=("build", "run"), when="@:1.40-2")
