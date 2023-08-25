# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RScattermore(RPackage):
    """Scatterplots with More Points.

    C-based conversion of large scatterplot data to rasters. Speeds up plotting
    of data with millions of points."""

    cran = "scattermore"

    version("0.8", sha256="dbdd73d8261cb063464bb29d5c17733b7e87bc50a19948bc80439e19f2a9f8e5")
    version("0.7", sha256="f36280197b8476314d6ce81a51c4ae737180b180204043d2937bc25bf3a5dfa2")

    depends_on("r-ggplot2", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
