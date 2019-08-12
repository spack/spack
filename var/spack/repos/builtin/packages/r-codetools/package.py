# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCodetools(RPackage):
    """Code analysis tools for R."""

    homepage = "https://cran.r-project.org/web/packages/codetools/index.html"
    url      = "https://cran.r-project.org/src/contrib/codetools_0.2-15.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/codetools"

    version('0.2-15', '37419cbc3de81984cf6d9b207d4f62d4')
    version('0.2-14', '7ec41d4f8bd6ba85facc8c5e6adc1f4d')
