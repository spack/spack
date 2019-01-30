# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNanotime(RPackage):
    """Full 64-bit resolution date and time support with resolution up to
       nanosecond granularity is provided, with easy transition to and from
       the standard 'POSIXct' type."""

    homepage = "https://cran.r-project.org/package=nanotime"
    url      = "https://cran.r-project.org/src/contrib/nanotime_0.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/nanotime"

    version('0.2.0', '796b1f7d0bb43e2f3d98e3cc6f4b0657')

    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-rcppcctz', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
