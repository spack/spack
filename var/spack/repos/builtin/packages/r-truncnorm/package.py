# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTruncnorm(RPackage):
    """Density, probability, quantile and random number generation functions
    for the truncated normal distribution."""

    homepage = "https://cloud.r-project.org/package=truncnorm"
    url      = "https://cloud.r-project.org/src/contrib/truncnorm_1.0-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/truncnorm"

    version('1.0-8', 'c60cd6555be0dd2ea91e61757439282d')

    depends_on('r@3.4.0:', type=('build', 'run'))
