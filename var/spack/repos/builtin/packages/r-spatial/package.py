# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSpatial(RPackage):
    """Functions for Kriging and Point Pattern Analysis.

    Functions for kriging and point pattern analysis."""

    cran = "spatial"

    version("7.3-15", sha256="e5613be94d6f5c1f54813dadc96e4a86b3417dea28106cc90cb24dfd6c3c8cef")
    version("7.3-12", sha256="7639039ee7407bd088e1b253376b2cb4fcdf4cc9124d6b48e4119d5cda872d63")
    version("7.3-11", sha256="624448d2ac22e1798097d09fc5dc4605908a33f490b8ec971fc6ea318a445c11")

    depends_on("r@3.0.0:", type=("build", "run"))

    depends_on("r-mass", type=("build", "run"), when="@:7.3-11")
