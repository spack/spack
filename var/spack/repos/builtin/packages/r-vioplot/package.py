# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RVioplot(RPackage):
    """Violin Plot.

    A violin plot is a combination of a box plot and a kernel density plot.
    This package allows extensive customisation of violin plots."""

    cran = "vioplot"

    version("0.3.7", sha256="06475d9a47644245ec91598e9aaef7db1c393802d9fc314420ac5139ae56adb6")
    version("0.3.5", sha256="1b64833c1bd6851036cf1c400c7d0036a047e71def94a399c897263b4b303e2a")
    version("0.3.2", sha256="7b51d0876903a3c315744cb051ac61920eeaa1f0694814959edfae43ce956e8e")

    depends_on("r+X", type=("build", "run"))
    depends_on("r-sm", type=("build", "run"))
    depends_on("r-zoo", type=("build", "run"))
