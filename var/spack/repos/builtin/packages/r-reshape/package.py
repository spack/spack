# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReshape(RPackage):
    """Flexibly restructure and aggregate data using just two functions: melt
       and cast."""

    homepage = "https://cran.r-project.org/package=reshape"
    url      = "https://cran.r-project.org/src/contrib/reshape_0.8.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/reshape"

    version('0.8.7', '0b0eececc5eb74dea9d59a985bce6211')

    depends_on('r-plyr', type=('build', 'run'))
