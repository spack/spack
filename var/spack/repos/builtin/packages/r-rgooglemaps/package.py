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

    homepage = "https://cloud.r-project.org/package=RgoogleMaps"
    url      = "https://cloud.r-project.org/src/contrib/RgoogleMaps_1.2.0.7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/RgoogleMaps"

    version('1.4.3', sha256='44cb62bcd23e5b4807e91c5825352eb8d38aaaeb3b38a8271ca9f21c1e1d4b19')
    version('1.4.2', sha256='b479996fcb72f067644a7ea7f00325e44e76efd202e84aaab022753c4a6d5584')
    version('1.2.0.7', '2e1df804f0331b4122d841105f0c7ea5')

    depends_on('r-png', type=('build', 'run'))
    depends_on('r-rjsonio@:1.3.9', type=('build', 'run'))
