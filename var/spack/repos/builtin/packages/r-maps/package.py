# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMaps(RPackage):
    """Display of maps. Projection code and larger maps are in separate
    packages ('mapproj' and 'mapdata')."""

    homepage = "https://cran.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/maps_3.1.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/maps"

    version('3.1.1', 'ff045eccb6d5a658db5a539116ddf764')
