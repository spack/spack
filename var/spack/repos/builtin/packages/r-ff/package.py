# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFf(RPackage):
    """memory-efficient storage of large data on disk and
    fast access functions."""

    homepage = "http://ff.r-forge.r-project.org/"
    url      = "https://cran.rstudio.com/src/contrib/ff_2.2-13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ff"

    version('2.2-13', '4adf8840d24cb6e2927a3ef885c86fcd')

    depends_on('r-bit', type=('build', 'run'))
