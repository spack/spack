# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RRmarkdown(RPackage):
    """Convert R Markdown documents into a variety of formats."""

    homepage = "http://rmarkdown.rstudio.com/"
    url      = "https://cran.r-project.org/src/contrib/rmarkdown_1.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/rmarkdown"

    version('1.7', '477c50840581ba7947b3d905c67a511b')
    version('1.0', '264aa6a59e9680109e38df8270e14c58')

    depends_on('r-knitr@1.14:', type=('build', 'run'))
    depends_on('r-yaml@2.1.5:', type=('build', 'run'))
    depends_on('r-htmltools@0.3.5:', type=('build', 'run'))
    depends_on('r-evaluate@0.8:', type=('build', 'run'))
    depends_on('r-base64enc', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-rprojroot', type=('build', 'run'))
    depends_on('r-mime', type=('build', 'run'))
    depends_on('r-stringr@1.2.0:', type=('build', 'run'))
    depends_on('r-catools', type=('build', 'run'))
    depends_on('r@3.0:')
