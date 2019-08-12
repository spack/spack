# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBackports(RPackage):
    """Implementations of functions which have been introduced
    in R since version 3.0.0. The backports are conditionally
    exported which results in R resolving the function names to
    the version shipped with R (if available) and uses the
    implemented backports as fallback. This way package developers
    can make use of the new functions without worrying about the
    minimum required R version."""

    homepage = "https://cran.r-project.org/package=backports"
    url      = "https://cran.r-project.org/src/contrib/backports_1.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/backports"

    version('1.1.1', '969543a0af32dc23bba9bb37ec82008c')
    version('1.1.0', 'b97a71b026fd7ede0e449be93d160c17')
