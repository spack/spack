# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RC50(RPackage):
    """C5.0 decision trees and rule-based models for pattern recognition."""

    homepage = "https://cran.r-project.org/package=C50"
    url      = "https://cran.r-project.org/src/contrib/C50_0.1.0-24.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/C50"

    version('0.1.0-24', '42631e65c5c579532cc6edf5ea175949')

    depends_on('r-partykit', type=('build', 'run'))
