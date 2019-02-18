# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSfsmisc(RPackage):
    """Useful utilities ['goodies'] from Seminar fuer Statistik
    ETH Zurich, quite a few related to graphics;
    some were ported from S-plus."""

    homepage = "https://cran.r-project.org/web/packages/sfsmisc/index.html"
    url      = "https://cran.r-project.org/src/contrib/sfsmisc_1.1-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sfsmisc"

    version('1.1-0', '1ba4303076e2bbf018f7eecc7d04e178')
