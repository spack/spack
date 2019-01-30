# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RExpm(RPackage):
    """Computation of the matrix exponential, logarithm, sqrt, and related
    quantities."""

    homepage = "http://R-Forge.R-project.org/projects/expm"
    url      = "https://cran.r-project.org/src/contrib/expm_0.999-2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/expm"

    version('0.999-2', 'e05fa3f995754af92bd03227625da984')
