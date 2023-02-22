# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RGgplot2(RPackage):
    """Create Elegant Data Visualisations Using the Grammar of Graphics.

    A system for 'declaratively' creating graphics, based on "The Grammar of
    Graphics". You provide the data, tell 'ggplot2' how to map variables to
    aesthetics, what graphical primitives to use, and it takes care of the
    details."""

    cran = "ggplot2"

    version("3.4.0", sha256="a82f9e52f974389439765f71a8206ec26e3be30a8864d2c784d5ea8abcb0473e")
    version("3.3.6", sha256="bfcb4eb92a0fcd3fab713aca4bb25e916e05914f2540271a45522ad7e43943a9")
    version("3.3.5", sha256="b075294faf3af31b18e415f260c62d6000b218770e430484fe38819bdc3224ea")
    version("3.3.3", sha256="45c29e2348dbd195bbde1197a52db7764113e57f463fd3770fb899acc33423cc")
    version("3.2.0", sha256="31b6897fb65acb37913ff6e2bdc1b57f652360098ae3aa660abdcf54f84d73b3")
    version("3.1.1", sha256="bfde297f3b4732e7f560078f4ce131812a70877e6b5b1d41a772c394939e0c79")
    version("2.2.1", sha256="5fbc89fec3160ad14ba90bd545b151c7a2e7baad021c0ab4b950ecd6043a8314")
    version("2.1.0", sha256="f2c323ae855d6c089e3a52138aa7bc25b9fe1429b8df9eae89d28ce3c0dd3969")

    depends_on("r@3.1:", type=("build", "run"))
    depends_on("r@3.2:", type=("build", "run"), when="@3.2.0:")
    depends_on("r@3.3:", type=("build", "run"), when="@3.3.4:")
    depends_on("r-cli", type=("build", "run"), when="@3.4.0:")
    depends_on("r-glue", type=("build", "run"), when="@3.3.3:")
    depends_on("r-gtable@0.1.1:", type=("build", "run"))
    depends_on("r-isoband", type=("build", "run"), when="@3.3.3:")
    depends_on("r-lifecycle@1.0.1:", type=("build", "run"), when="@3.4.0:")
    depends_on("r-mass", type=("build", "run"))
    depends_on("r-mgcv", type=("build", "run"), when="@3.2.0:")
    depends_on("r-rlang@0.3.0:", type=("build", "run"), when="@3.0.0:")
    depends_on("r-rlang@0.4.10:", type=("build", "run"), when="@3.3.4:")
    depends_on("r-rlang@1.0.0:", type=("build", "run"), when="@3.4.0:")
    depends_on("r-scales@0.5.0:", type=("build", "run"))
    depends_on("r-scales@1.2.0:", type=("build", "run"), when="@3.4.0:")
    depends_on("r-tibble", type=("build", "run"))
    depends_on("r-vctrs@0.5.0:", type=("build", "run"), when="@3.4.0:")
    depends_on("r-withr@2.0.0:", type=("build", "run"), when="@3.0.0:")
    depends_on("r-withr@2.5.0:", type=("build", "run"), when="@3.4.0:")

    depends_on("r-plyr@1.7.1:", type=("build", "run"), when="@:3.1.1")
    depends_on("r-reshape2", type=("build", "run"), when="@:3.2.0")
    depends_on("r-lazyeval", type=("build", "run"), when="@:3.2.0")
    depends_on("r-viridislite", type=("build", "run"), when="@3.0.0:3.2.0")
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-digest", when="@:3.3.6")
