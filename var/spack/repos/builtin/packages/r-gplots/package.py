# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

#
#
from spack import *


class RGplots(RPackage):
    """Various R Programming Tools for Plotting Data."""

    homepage = "https://cran.r-project.org/package=gplots"
    url      = "https://cran.rstudio.com/src/contrib/gplots_3.0.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/gplots"
    version('3.0.1', '6116822401d55add044beb120ca93d14')
    depends_on('r-gtools', type=('build', 'run'))
    depends_on('r-gdata', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r-kernsmooth', type=('build', 'run'))
