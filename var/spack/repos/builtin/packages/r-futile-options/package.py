# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFutileOptions(RPackage):
    """A scoped options management framework"""

    homepage = "https://cran.rstudio.com/web/packages/futile.options/index.html"
    url      = "https://cran.rstudio.com/src/contrib/futile.options_1.0.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/futile.options"

    version('1.0.0', '8fd845774bbce56f41f7c43c3b4c13ba')
