# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSvglite(RPackage):
    """An 'SVG' Graphics Device.

    A graphics device for R that produces 'Scalable Vector Graphics'. 'svglite'
    is a fork of the older 'RSvgDevice' package."""

    cran = "svglite"

    version("2.1.0", sha256="ad40f590c7e80ae83001a3826b6e8394ba733446ed51fd55faeda974ab839c9b")
    version("2.0.0", sha256="76e625fe172a5b7ce99a67b6d631b037b3f7f0021cfe15f2e15e8851b89defa5")

    depends_on("r+X", type=("build", "run"))
    depends_on("r@3.0.0:", type=("build", "run"))
    depends_on("r-systemfonts@1.0.0:", type=("build", "run"))
    depends_on("r-cpp11", type=("build", "run"))
    depends_on("libpng")
