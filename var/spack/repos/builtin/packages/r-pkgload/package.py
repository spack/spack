# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RPkgload(RPackage):
    """Simulate Package Installation and Attach.

    Simulates the process of installing a package and then attaching it. This
    is a key part of the 'devtools' package as it allows you to rapidly iterate
    while developing a package."""

    cran = "pkgload"

    version("1.3.1", sha256="c6b8b70d7b7e194e7d44a42364f0362e971d9ab9c5794c4ae5ed4f9e61b1679a")
    version("1.3.0", sha256="5af653c901662260cc221971cc968355428cc6183b61c15be80aa9545f9f4228")
    version("1.2.4", sha256="d6912bc824a59ccc9b2895c3cf3b08a3ff310a333888bb8e90d1a6ce754dd90f")
    version("1.1.0", sha256="189d460dbba2b35fa15dd59ce832df252dfa654a5acee0c9a8471b4d70477b0d")
    version("1.0.2", sha256="3186564e690fb05eabe76e1ac0bfd4312562c3ac8794b29f8850399515dcf27c")

    depends_on("r@3.4.0:", type=("build", "run"), when="@1.3.0:")

    depends_on("r-cli", type=("build", "run"), when="@1.1.0:")
    depends_on("r-cli@3.3.0:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-crayon", type=("build", "run"), when="@1.1.0:")
    depends_on("r-desc", type=("build", "run"))
    depends_on("r-glue", type=("build", "run"), when="@1.3.0:")
    depends_on("r-fs", type=("build", "run"), when="@1.3.0:")
    depends_on("r-rlang", type=("build", "run"))
    depends_on("r-rlang@1.0.3:", type=("build", "run"), when="@1.3.0:")
    depends_on("r-rprojroot", type=("build", "run"))
    depends_on("r-withr", type=("build", "run"))
    depends_on("r-withr@2.4.3:", type=("build", "run"), when="@1.3.0:")

    depends_on("r-pkgbuild", type=("build", "run"), when="@:1.1.0")
    depends_on("r-rstudioapi", type=("build", "run"))
    depends_on("r-rstudioapi", when="@:1.2.4")
    depends_on("r-rstudioapi", when="@:1.3.0")
