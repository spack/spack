# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RSp(RPackage):
    """Classes and methods for spatial data; the classes document where the
    spatial location information resides, for 2D or 3D data. Utility functions
    are provided, e.g. for plotting data as maps, spatial selection, as well as
    methods for retrieving coordinates, for subsetting, print, summary, etc."""

    homepage = "https://github.com/edzer/sp/"
    url      = "https://cloud.r-project.org/src/contrib/sp_1.2-3.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/sp"

    version('1.2-7', sha256='6d60e03e1abd30a7d4afe547d157ce3dd7a8c166fc5e407fd6d62ae99ff30460')
    version('1.2-3', 'f0e24d993dec128642ee66b6b47b10c1')

    depends_on('r-lattice', type=('build', 'run'))
