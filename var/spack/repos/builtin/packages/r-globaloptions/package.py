# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGlobaloptions(RPackage):
    """It provides more controls on the option values such as validation and
       filtering on the values, making options invisible or private."""

    homepage = "https://cran.r-project.org/package=GlobalOptions"
    url      = "https://cran.rstudio.com/src/contrib/GlobalOptions_0.0.12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/GlobalOptions"

    version('0.0.12', '6c268b3b27874918ba62eb0f6aa0a3e5')

    depends_on('r-testthat', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-markdown', type=('build', 'run'))
