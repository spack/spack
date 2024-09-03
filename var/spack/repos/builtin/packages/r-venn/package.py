# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVenn(RPackage):
    """
    A close to zero dependency package to draw and display Venn diagrams
    up to 7 sets, and any Boolean union of set intersections.
    """

    homepage = "https://cran.r-project.org/package=venn"
    cran = "venn"

    version("1.12", sha256="ed86b69bd99ceea93352a30699a0baba3fd8cdcde907a9476e92be202ad8721d")
    version("1.11", sha256="33d915c7c90078f1e76e803fa3f02ab5b74dd04de7a9700477e51e0235f19314")
    version("1.10", sha256="65422a158cdc8581182d3d326e448e43ecc3764501a5dab1ccac1234b4f961e4")
    version("1.9", sha256="19c96cd7daad83267c666106ceea742dbc1eed917922ce61b2088b9198e45b34")
    version("1.8", sha256="c932a7339aa5f4899c89885504bb5c0ea6cf4f55869079a877be96387538e41d")

    depends_on("r@3.5:")
    depends_on("r-admisc@0.33:")
