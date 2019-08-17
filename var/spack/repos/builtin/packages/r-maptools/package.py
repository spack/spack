# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMaptools(RPackage):
    """Set of tools for manipulating and reading geographic data, in particular
    ESRI shapefiles; C code used from shapelib. It includes binary access to
    GSHHG shoreline files. The package also provides interface wrappers for
    exchanging spatial objects with packages such as PBSmapping, spatstat,
    maps, RArcInfo, Stata tmap, WinBUGS, Mondrian, and others."""

    homepage = "http://r-forge.r-project.org/projects/maptools/"
    url      = "https://cran.r-project.org/src/contrib/maptools_0.8-39.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/maptools"

    version('0.8-39', '3690d96afba8ef22c8e27ae540ffb836')

    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-foreign', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
