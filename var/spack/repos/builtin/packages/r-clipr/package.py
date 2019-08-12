# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClipr(RPackage):
    """Simple utility functions to read from and write to the Windows, OS X,
       and X11 clipboards."""

    homepage = "https://github.com/mdlincoln/clipr"
    url      = "https://cran.r-project.org/src/contrib/clipr_0.4.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/clipr"

    version('0.4.0', '4012a31eb3b7a36bd3bac00f916e56a7')

    depends_on('r-rstudioapi', type=('build', 'run'))
    depends_on('r-testthat', type=('build', 'run'))
    depends_on('xclip')
