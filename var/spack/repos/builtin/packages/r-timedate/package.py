# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RTimedate(RPackage):
    """Rmetrics - Chronological and Calendar Objects.

    The 'timeDate' class fulfils the conventions of the ISO 8601 standard as
    well as of the ANSI C and POSIX standards. Beyond these standards it
    provides the "Financial Center" concept which allows to handle data records
    collected in different time zones and mix them up to have always the proper
    time stamps with respect to your personal financial center, or
    alternatively to the GMT reference time. It can thus also handle time
    stamps from historical data records from the same time zone, even if the
    financial centers changed day light saving times at different calendar
    dates."""

    cran = "timeDate"

    version('3043.102', sha256='377cba03cddab8c6992e31d0683c1db3a73afa9834eee3e95b3b0723f02d7473')
    version('3042.101', sha256='6c8d4c7689b31c6a43555d9c7258516556ba03b132e5643691e3e317b89a8c6d')
    version('3012.100', sha256='6262ef7ca9f5eeb9db8229d6bb7a51d46d467a4fa73e2ccc5b4b78e18780c432')

    depends_on('r@2.15.1:', type=('build', 'run'))
