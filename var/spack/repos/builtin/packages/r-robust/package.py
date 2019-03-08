# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)
# See the Spack documentation for more information on packaging.

from spack import *


class RRobust(RPackage):
    """robust: Port of the S+ Robust Library """

    homepage = "https://cran.r-project.org/package=robust"
    url      = "https://cran.r-project.org/src/contrib/robust_0.4-18.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/robust/"

    version('0.4-18', sha256='e4196f01bb3b0d768759d4411d524238b627eb8dc213d84cb30014e75480f8ac')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-robustbase', type=('build', 'run'))
    depends_on('r-rrcov', type=('build', 'run'))
    depends_on('r-fit-models', type=('build', 'run'))
