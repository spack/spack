# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RDichromat(RPackage):
    """Color Schemes for Dichromats.

    Collapse red-green or green-blue distinctions to simulate the effects of
    different types of color-blindness."""

    cran = "dichromat"

    version('2.0-0', sha256='31151eaf36f70bdc1172da5ff5088ee51cc0a3db4ead59c7c38c25316d580dd1')

    depends_on('r@2.10:', type=('build', 'run'))
