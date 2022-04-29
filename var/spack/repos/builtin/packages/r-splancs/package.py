# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.pkgkit import *


class RSplancs(RPackage):
    """Spatial and Space-Time Point Pattern Analysis.

    The Splancs package was written as an enhancement to S-Plus for display and
    analysis of spatial point pattern data; it has been ported to R and is in
    "maintenance mode"."""

    cran = "splancs"

    version('2.01-42', sha256='8c0af4764521e20b629dba6afd5c284e7be48786f378c37668eacfa26d2ef0aa')
    version('2.01-40', sha256='79744381ebc4a361740a36dca3c9fca9ae015cfe0bd585b7856a664a3da74363')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-sp@0.9:', type=('build', 'run'))
