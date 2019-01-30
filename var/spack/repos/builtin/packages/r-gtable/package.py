# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGtable(RPackage):
    """Tools to make it easier to work with "tables" of 'grobs'."""

    homepage = "https://cran.r-project.org/web/packages/gtable/index.html"
    url      = "https://cran.r-project.org/src/contrib/gtable_0.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gtable"

    version('0.2.0', '124090ae40b2dd3170ae11180e0d4cab')
