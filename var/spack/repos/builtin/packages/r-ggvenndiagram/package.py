# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgvenndiagram(RPackage):
    """Tools and Plots for Multi-Well Plates."""

    homepage = "https://cran.r-project.org/package=ggVennDiagram"
    cran = "ggVennDiagram"

    version("1.5.2", sha256="d162f0caa19041dbe6db605e90876d3c534ed6d976dba29309f60f37da5df243")

    depends_on("r@4.1:")
    depends_on("r-sf")
    depends_on("r-ggplot2@3.4:")
    depends_on("r-dplyr")
    depends_on("r-magrittr")
    depends_on("r-purrr")
    depends_on("r-tibble")
    depends_on("r-plotly")
    depends_on("r-venn@1.12:")
    depends_on("r-rvenn")
    depends_on("r-yulab-utils")
    depends_on("r-aplot")
    depends_on("r-forcats")
