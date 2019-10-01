# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRsolnp(RPackage):
    """General Non-linear Optimization Using Augmented Lagrange Multiplier
    Method."""

    homepage = "https://cloud.r-project.org/package=Rsolnp"
    url      = "https://cloud.r-project.org/src/contrib/Rsolnp_1.16.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/Rsolnp"

    version('1.16', '507e1e1a64f5f1d32b7e4e12ed19599f')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('r-truncnorm', type=('build', 'run'))
