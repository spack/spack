# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cloud.r-project.org/src/contrib/reprex_0.1.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/reprex"

    version('0.2.1', sha256='5d234ddfbcadc5a5194a58eb88973c51581e7e2e231f146974af8f42747b45f3')
    version('0.1.1', 'fcd89995d7b35a2ddd4269973937bde3')

    depends_on('r-callr@2.0.0:', type=('build', 'run'))
    depends_on('r-clipr@0.4.0:', type=('build', 'run'))
    depends_on('r-knitr', when='@:0.1.9', type=('build', 'run'))
    depends_on('r-rmarkdown', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
    depends_on('r-rlang', when='@0.2.0:', type=('build', 'run'))
    depends_on('r-withr', when='@0.2.0:', type=('build', 'run'))
    depends_on('r-fs', when='@0.2.1:', type=('build', 'run'))
