# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGeosphere(RPackage):
    """Spherical Trigonometry.

    Spherical trigonometry for geographic applications. That is, compute
    distances and related measures for angular (longitude/latitude)
    locations."""

    cran = "geosphere"

    version("1.5-14", sha256="f2c3a4ae1c87c86c123d48f134721c809fb33675cb5cd0959080049eabdbe42d")
    version("1.5-10", sha256="56cd4f787101e2e18f19ddb83794154b58697e63cad81168f0936f60ab7eb497")
    version("1.5-7", sha256="9d9b555e2d59a5ae174ae654652121f169fbc3e9cf66c2491bfbe0684b6dd8a0")
    version("1.5-5", sha256="8b6fe012744fc45b88e0ef6f20e60e103ef013e761e99dcff3f9dceeedbdce6d")

    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-sp", type=("build", "run"))
