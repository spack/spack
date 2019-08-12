# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RForcats(RPackage):
    """Helpers for reordering factor levels (including moving specified levels
       to front, ordering by first appearance, reversing, and randomly
       shuffling), and tools for modifying factor levels (including collapsing
       rare levels into other, 'anonymising', and manually 'recoding')."""

    homepage = "http://forcats.tidyverse.org/"
    url      = "https://cran.r-project.org/src/contrib/forcats_0.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/forcats"

    version('0.2.0', 'e4ba2c0a59dcdfcc02274c519bf3dbfc')

    depends_on('r-tibble', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
