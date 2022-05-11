# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RGgmap(RPackage):
    """Spatial Visualization with ggplot2.

    A collection of functions to visualize spatial data and models on top of
    static maps from various online sources (e.g Google Maps and Stamen Maps).
    It includes tools common to those tasks, including functions for
    geolocation and routing."""

    cran = "ggmap"

    version('3.0.0', sha256='96c24ffdc0710d0633ac4721d599d2c06f43a29c59d1e85c94ff0af30dfdb58d')
    version('2.6.2', sha256='4e9cf53ab108fc70805d971dadb69b26fe67ea289c23c38adf6e30b198379d90')
    version('2.6.1', sha256='fc450ef422005fc7d2018a34f6b410fbdf80824f9ed60351d91205c413585a57')

    depends_on('r@3.1.0:', type=('build', 'run'))
    depends_on('r-ggplot2@2.2.0:', type=('build', 'run'))
    depends_on('r-rgooglemaps', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-rjson', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
    depends_on('r-dplyr', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-bitops', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-glue', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-httr', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-stringr', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-purrr', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-magrittr', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-tibble', type=('build', 'run'), when='@3.0.0:')
    depends_on('r-tidyr', type=('build', 'run'), when='@3.0.0:')

    depends_on('r-proto', type=('build', 'run'), when='@:2.6.2')
    depends_on('r-reshape2', type=('build', 'run'), when='@:2.6.2')
    depends_on('r-mapproj', type=('build', 'run'), when='@:2.6.2')
    depends_on('r-geosphere', type=('build', 'run'), when='@:2.6.2')
