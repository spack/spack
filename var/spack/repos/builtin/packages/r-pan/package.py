# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPan(RPackage):
    """Multiple imputation for multivariate panel or clustered data."""

    homepage = "https://cran.r-project.org/package=pan"
    url      = "https://cran.r-project.org/src/contrib/pan_1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/pan"

    version('1.4', 'cdead963110561fc42dc544a60ac44ed')
