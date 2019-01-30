# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDevtools(RPackage):
    """Collection of package development tools."""

    homepage = "https://github.com/hadley/devtools"
    url      = "https://cran.r-project.org/src/contrib/devtools_1.12.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/devtools"

    version('1.12.0', '73b46c446273566e5b21c9f5f72aeca3')
    version('1.11.1', '242672ee27d24dddcbdaac88c586b6c2')

    depends_on('r@3.0.2:')

    depends_on('r-httr@0.4:', type=('build', 'run'))
    depends_on('r-memoise@1.0.0:', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
    depends_on('r-digest', type=('build', 'run'))
    depends_on('r-rstudioapi@0.2.0:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'))
    depends_on('r-git2r@0.11.0:', type=('build', 'run'))
    depends_on('r-withr', type=('build', 'run'))
