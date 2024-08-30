# Copyright 2013-2024 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RKableextra(RPackage):
    """Construct Complex Table with 'kable' and Pipe Syntax.

    Build complex HTML or 'LaTeX' tables using 'kable()' from 'knitr' and the
    piping syntax from 'magrittr'. Function 'kable()' is a light weight table
    generator coming from 'knitr'. This package simplifies the way to
    manipulate the HTML or 'LaTeX' codes generated by 'kable()' and allows
    users to construct complex tables and customize styles using a readable
    syntax."""

    cran = "kableExtra"

    version("1.4.0", sha256="8fe2cc9fc2e8991685c4dc9e4904459e6f572c945319befde36d76f3ab527409")
    version("1.3.4", sha256="091ffac282cf9257edcec1a06da38b5e6516f111296bedb934e32f5692ffbbb0")

    depends_on("r@3.1.0:", type=("build", "run"))
    depends_on("r-knitr@1.16:", type=("build", "run"))
    depends_on("r-knitr@1.33:", type=("build", "run") , when="@1.4.0:")
    depends_on("r-magrittr", type=("build", "run"))
    depends_on("r-stringr@1.0:", type=("build", "run"))
    depends_on("r-xml2@1.1.1:", type=("build", "run"))
    depends_on("r-rmarkdown@1.6.0:", type=("build", "run"))
    depends_on("r-scales", type=("build", "run"))
    depends_on("r-viridislite", type=("build", "run"))
    depends_on("r-htmltools", type=("build", "run"))
    depends_on("r-rstudioapi", type=("build", "run"))
    depends_on("r-digest", type=("build", "run"))
    depends_on("r-svglite", type=("build", "run"))

    depends_on("r-rvest", type=("build", "run"), when="@:1.3.4")
    depends_on("r-glue", type=("build", "run"), when="@:1.3.4")
    depends_on("r-webshot", type=("build", "run"), when="@:1.3.4")
