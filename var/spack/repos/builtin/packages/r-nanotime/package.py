# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package import *


class RNanotime(RPackage):
    """Nanosecond-Resolution Time Support for R.

    Full 64-bit resolution date and time functionality with; nanosecond
    granularity is provided, with easy transition to and from; the standard
    'POSIXct' type. Three additional classes offer interval,; period and
    duration functionality for nanosecond-resolution timestamps."""

    cran = "nanotime"

    version('0.3.5', sha256='44deaae58452bacea4855d018212593811401c2afc460ffb11905479013923a0')
    version('0.3.2', sha256='9ef53c3bca01b605a9519190117988e170e63865327007c90b05d31fe7f22b1d')
    version('0.2.4', sha256='2dfb7e7435fec59634b87563a215467e7793e2711e302749c0533901c74eb184')
    version('0.2.3', sha256='7d6df69a4223ae154f610b650e24ece38ce4aa706edfa38bec27d15473229f5d')
    version('0.2.0', sha256='9ce420707dc4f0cb4241763579b849d842904a3aa0d88de8ffef334d08fa188d')

    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-rcppcctz@0.2.3:', type=('build', 'run'))
    depends_on('r-rcppcctz@0.2.9:', type=('build', 'run'), when='@0.3.2:')
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'), when='@0.3.2:')
    depends_on('r-rcppdate', type=('build', 'run'), when='@0.3.2:')
