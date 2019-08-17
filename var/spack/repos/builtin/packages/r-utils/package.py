# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RUtils(RPackage):
    """Utility functions useful when programming and
    developing R packages."""

    homepage = "https://github.com/HenrikBengtsson/R.utils"
    url      = "https://cran.rstudio.com/src/contrib/R.utils_2.5.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/R.utils"

    version('2.5.0', 'a728ef3ceb35cafc4c39ea577cecc38b')

    depends_on('r-oo', type=('build', 'run'))
