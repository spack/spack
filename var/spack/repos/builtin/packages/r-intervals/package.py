# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RIntervals(RPackage):
    """Tools for working with and comparing sets of points and intervals."""

    cran = "intervals"

    version("0.15.3", sha256="8501fef7c74b9be874e807839518aae85e79bf4a047cd52169b52c6d9b41dfc4")
    version("0.15.2", sha256="0bd23b0ce817ddd851238233d8a5420bf3a6d29e75fd361418cbc50118777c57")
    version("0.15.1", sha256="9a8b3854300f2055e1492c71932cc808b02feac8c4d3dbf6cba1c7dbd09f4ae4")

    depends_on("r@2.9.0:", type=("build", "run"))
