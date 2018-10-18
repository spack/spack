# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReprex(RPackage):
    """Convenience wrapper that uses the 'rmarkdown' package to render small
       snippets of code to target formats that include both code and output.
       The goal is to encourage the sharing of small, reproducible, and
       runnable examples on code-oriented websites, such as
       <http://stackoverflow.com> and <https://github.com>, or in email.
       'reprex' also extracts clean, runnable R code from various common
       formats, such as copy/paste from an R session."""

    homepage = "https://github.com/jennybc/reprex"
    url      = "https://cran.r-project.org/src/contrib/reprex_0.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/reprex"

    version('0.1.1', 'fcd89995d7b35a2ddd4269973937bde3')

    depends_on('r-callr', type=('build', 'run'))
    depends_on('r-clipr', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rmarkdown', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
