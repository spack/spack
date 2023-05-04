# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTruncnorm(RPackage):
    """Truncated Normal Distribution.

    Density, probability, quantile and random number generation functions for
    the truncated normal distribution."""

    cran = "truncnorm"

    version("1.0-8", sha256="49564e8d87063cf9610201fbc833859ed01935cc0581b9e21c42a0d21a47c87e")
    version("1.0.0", sha256="dc1b018cb6d9ad5beb2d9e2f3ebe56c3f69d7a98fc5a1d963dd7933d209ac272")

    depends_on("r@2.7.0:", type=("build", "run"))
    depends_on("r@3.4.0:", type=("build", "run"), when="@1.0-8:")
