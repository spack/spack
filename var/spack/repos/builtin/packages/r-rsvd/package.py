# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsvd(RPackage):
    """rsvd: Randomized Singular Value Decomposition"""

    homepage = "https://github.com/erichson/rSVD"
    url      = "https://cran.r-project.org/src/contrib/rsvd_1.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rsvd"

    version('1.0.1', sha256='ffb7d8a7360a8cf265e43c481abdcde3091460d592e270924b7209591c9c5ab9')

    depends_on('r@3.2.2:', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
