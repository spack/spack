# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUdunits2(RPackage):
    """Provides simple bindings to Unidata's udunits library."""

    homepage = "https://github.com/pacificclimate/Rudunits2"
    url      = "https://cloud.r-project.org/src/contrib/udunits2_0.13.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/udunits2"

    version('0.13', 'c8717808c740ef70eed7aea93c7c4c7d')

    depends_on('r@2.10.0:', type=('build', 'run'))
    depends_on('udunits2')
