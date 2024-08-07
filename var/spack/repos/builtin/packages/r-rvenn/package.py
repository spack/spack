# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RRvenn(RPackage):
    """Tools and Plots for Multi-Well Plates."""

    homepage = "https://cran.r-project.org/package=RVenn"
    cran = "RVenn"

    version("1.1.0", sha256="c41a96dd4a9b51e7dcc8647cdbaa0faa704ab22d5b0c1d45e593a6b23b00d504")
    version("1.0.0", sha256="8f67b871b242031e09c86c838874c3db009cdb5045b95e6e871fb9233fd261da")

    depends_on("r-ggforce@0.2.1:")
    depends_on("r-ggplot2@3.0.0:")
    depends_on("r-magrittr@1.5:")
    depends_on("r-purrr@0.2.5:")
    depends_on("r-rlang@0.2.2:")
    depends_on("r-vegan@2.5.2:")
    depends_on("r-pheatmap@1.0.10:")
