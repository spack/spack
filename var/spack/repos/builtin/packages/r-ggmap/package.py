# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGgmap(RPackage):
    """A collection of functions to visualize spatial data and models on top of
    static maps from various online sources (e.g Google Maps and Stamen Maps).
    It includes tools common to those tasks, including functions for
    geolocation and routing."""

    homepage = "https://github.com/dkahle/ggmap"
    url      = "https://cran.r-project.org/src/contrib/ggmap_2.6.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggmap"

    version('2.6.1', '25ad414a3a1c6d59a227a9f22601211a')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-proto', type=('build', 'run'))
    depends_on('r-rgooglemaps', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-reshape2', type=('build', 'run'))
    depends_on('r-rjson', type=('build', 'run'))
    depends_on('r-mapproj', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-geosphere', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
