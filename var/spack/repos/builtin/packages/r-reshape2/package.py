# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RReshape2(RPackage):
    """Flexibly restructure and aggregate data using just two functions: melt
    and dcast (or acast)."""

    homepage = "https://github.com/hadley/reshape"
    url      = "https://cran.r-project.org/src/contrib/reshape2_1.4.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/reshape2"

    version('1.4.2', 'c851a0312191b8c5bab956445df7cf5f')
    version('1.4.1', '41e9dffdf5c6fa830321ac9c8ebffe00')

    depends_on('r-plyr', type=('build', 'run'))
    depends_on('r-stringr', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
