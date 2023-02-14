# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGparotation(RPackage):
    """GPA Factor Rotation.

    Gradient Projection Algorithm Rotation for Factor Analysis. See
    GPArotation.Intro for more details."""

    cran = "GPArotation"

    version("2022.10-2", sha256="04f72d8f3a9c204df5df904be563ec272a8437a707daee8823b2a690dde21917")
    version("2022.4-1", sha256="231e7edcdcc091fbecfb4f2e88d1a4344967cf7ea58074b385a4b8b48d9da224")
    version("2014.11-1", sha256="351bc15fc8dc6c8ea5045fbba22180d1e68314fc34d267545687748e312e5096")

    depends_on("r@2.0.0:", type=("build", "run"))
