# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDendextend(RPackage):
    """dendextend: Extending 'Dendrogram' Functionality in R"""

    homepage = "https://CRAN.R-project.org/package=dendextend"
    url      = "https://cran.r-project.org/src/contrib/dendextend_1.5.2.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/dendextend"

    version('1.5.2', '1134869d94005727c63cf3037e2f1bbf')

    depends_on('r@3.0.0:')
    depends_on('r-magrittr@1.0.1:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-fpc', type=('build', 'run'))
    depends_on('r-whisker', type=('build', 'run'))
    depends_on('r-viridis', type=('build', 'run'))
