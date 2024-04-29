# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RMatlab(RPackage):
    """MATLAB emulation package.

    Emulate MATLAB code using R."""

    cran = "matlab"

    license("Artistic-2.0")

    version("1.0.4", sha256="1988a2220703444a575f2bad4eb090a0da71478599eb53081dd7237b7ec216ea")
    version("1.0.2", sha256="a23dec736c51ae1864c1a53caac556a2f98e8020138a3b121badb0f5b7984154")

    depends_on("r@2.15:", type=("build", "run"))
