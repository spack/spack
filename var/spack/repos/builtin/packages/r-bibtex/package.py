# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RBibtex(RPackage):
    """Bibtex Parser.

    Utility to parse a bibtex file."""

    cran = "bibtex"

    version("0.5.0", sha256="ec81b4ee5b43f2114afd18d266f4633451abe20013422eb03848f00924b79167")
    version("0.4.2.3", sha256="7bad194920b412781ac9754ad41058d52d3cd7186e1851c2bce3640490e9bc6d")
    version("0.4.2", sha256="1f06ab3660c940405230ad16ff6e4ba38d4418a59cd9b16d78a4349f8b488372")

    depends_on("r@3.0.2:", type=("build", "run"))
    depends_on("r-backports@1.4.0:", type=("build", "run"), when="@0.5.0:")
    depends_on("r-stringr", type=("build", "run"))
    depends_on("r-stringr", when="@:0.4.2.3")
