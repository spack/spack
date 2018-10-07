# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSandwich(RPackage):
    """Model-robust standard error estimators for cross-sectional, time series,
    and longitudinal data."""

    homepage = "https://cran.r-project.org/package=sandwich"
    url      = "https://cran.r-project.org/src/contrib/sandwich_2.3-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sandwich"

    version('2.3-4', 'a621dbd8a57b6e1e036496642aadc2e5')

    depends_on('r@2.0.0:')

    depends_on('r-zoo', type=('build', 'run'))
