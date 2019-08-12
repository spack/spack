# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRgooglemaps(RPackage):
    """This package serves two purposes: (i) Provide a comfortable R interface
    to query the Google server for static maps, and (ii) Use the map as a
    background image to overlay plots within R. This requires proper coordinate
    scaling."""

    homepage = "https://cran.r-project.org/package=RgoogleMaps"
    url      = "https://cran.r-project.org/src/contrib/RgoogleMaps_1.2.0.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RgoogleMaps"

    version('1.2.0.7', '2e1df804f0331b4122d841105f0c7ea5')

    depends_on('r-png', type=('build', 'run'))
    depends_on('r-rjsonio', type=('build', 'run'))
