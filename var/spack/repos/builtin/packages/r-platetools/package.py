# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPlatetools(RPackage):
    """Tools and Plots for Multi-Well Plates."""

    homepage = "https://cran.r-project.org/package=platetools"
    cran = "platetools"

    version("0.1.7", sha256="ab20dc75b72392d8e305abbd86a9698891a73dc7e24b361abe627ce4cd8091f8")
    version("0.1.5", sha256="32abb2dcd413aad9fecd957af2abf0d6d41cd3dc3211c37be5ec08e7503ef863")
    version("0.1.3", sha256="0cd8ff28fe50de261eeb346445151746a070afe9d85af4aa594f87a1dceb0bb0")
    version("0.1.2", sha256="be6ce1d205261c33d455ff639f2d21d236cc03bf92cbfc090b798cc87a07d108")
    version("0.1.1", sha256="a073f1ed058863e774a07bd5160ea5fe25921358222b37211a265ff6e3084b4c")
    version("0.1.0", sha256="076c930bd12c77f84f8a74c6b06f7436caabf2457b8ed176e0a92878350ca0b3")
    version("0.0.2", sha256="eaea269695ca93151def65c16f10fe0ed022eaa4df1f872c5ef241d9061c5675")
    version("0.0.1", sha256="2bc3959e3cf663aab1560ee75afb928cd5ec305fa4899a75361bc3377e8a00f2")

    depends_on("r@3.1:")
    depends_on("r-ggplot2@2.2.0:")
    depends_on("r-rcolorbrewer")
