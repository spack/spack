# Copyright 2013-2023 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RSass(RPackage):
    """Syntactically Awesome Style Sheets ('Sass').

    An 'SCSS' compiler, powered by the 'LibSass' library. With this, R
    developers can use variables, inheritance, and functions to generate
    dynamic style sheets. The package uses the 'Sass CSS' extension language,
    which is stable, powerful, and CSS compatible."""

    cran = "sass"

    version("0.4.2", sha256="b409049d0de9fae853f46c19d353226c8e9244ce847bdada033d8669fc2c9646")
    version("0.4.1", sha256="850fcb6bd49085d5afd25ac18da0744234385baf1f13d8c0a320f4da2de608bb")
    version("0.4.0", sha256="7d06ca15239142a49e88bb3be494515abdd8c75f00f3f1b0ee7bccb55019bc2b")

    depends_on("r-fs", type=("build", "run"))
    depends_on("r-rlang@0.4.10:", type=("build", "run"))
    depends_on("r-htmltools@0.5.1:", type=("build", "run"))
    depends_on("r-r6", type=("build", "run"))
    depends_on("r-rappdirs", type=("build", "run"))
    depends_on("gmake", type="build")
