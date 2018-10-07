# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUnits(RPackage):
    """Support for measurement units in R vectors, matrices and arrays:
       automatic propagation, conversion, derivation and simplification of
       units; raising errors in case of unit incompatibility. Compatible with
       the POSIXct, Date and difftime classes. Uses the UNIDATA udunits
       library and unit database for unit compatibility checking and
       conversion."""

    homepage = "https://github.com/edzer/units/"
    url      = "https://cran.r-project.org/src/contrib/units_0.4-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/units"

    version('0.4-6', '0bb90dde5dad7608fa6feb1599381bf2')

    depends_on('r-udunits2', type=('build', 'run'))
