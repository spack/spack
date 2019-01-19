# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTidyselect(RPackage):
    """A backend for the selecting functions of the 'tidyverse'. It makes it
       easy to implement select-like functions in your own packages in a way
       that is consistent with other 'tidyverse' interfaces for selection."""

    homepage = "https://cran.r-project.org/package=tidyselect"
    url      = "https://cran.r-project.org/src/contrib/tidyselect_0.2.3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/tidyselect"

    version('0.2.3', 'c9dbd895ad7ce209bacfad6d19de91c9')

    depends_on('r-glue', type=('build', 'run'))
    depends_on('r-purrr', type=('build', 'run'))
    depends_on('r-rlang@0.1:', type=('build', 'run'))
    depends_on('r-rcpp@0.12.0:', type=('build', 'run'))
