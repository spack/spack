# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RHtmltools(RPackage):
    """Tools for HTML generation and output."""

    homepage = "https://github.com/rstudio/htmltools"
    url      = "https://cran.rstudio.com/src/contrib/htmltools_0.3.6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/htmltools"

    version('0.3.6', '336419c2143f958862e01ef1bbc9c253')
    version('0.3.5', '5f001aff4a39e329f7342dcec5139724')

    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
