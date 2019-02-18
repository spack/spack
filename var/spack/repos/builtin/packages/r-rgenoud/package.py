# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRgenoud(RPackage):
    """A genetic algorithm plus derivative optimizer."""

    homepage = "http://sekhon.berkeley.edu/rgenoud/"
    url      = "https://cran.r-project.org/src/contrib/rgenoud_5.8-1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rgenoud"

    version('5.8-1.0', '85801093d2f1e6789683b46ab4a7d70f')
