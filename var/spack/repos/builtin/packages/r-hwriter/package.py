# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHwriter(RPackage):
    """Easy-to-use and versatile functions to
    output R objects in HTML format."""

    homepage = "https://cran.rstudio.com/web/packages/hwriter/index.html"
    url      = "https://cran.rstudio.com/src/contrib/hwriter_1.3.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/hwriter"
    version('1.3.2', '9eef49df2eb68bbf3a16b5860d933517')
