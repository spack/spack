# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCowplot(RPackage):
    """Some helpful extensions and modifications to the 'ggplot2'
    package. In particular, this package makes it easy to combine
    multiple 'ggplot2' plots into one and label them with letters,
    e.g. A, B, C, etc., as is often required for scientific
    publications. The package also provides a streamlined and clean
    theme that is used in the Wilke lab, hence the package name,
    which stands for Claus O. Wilke's plot package."""

    homepage = "https://cran.r-project.org/package=cowplot"
    url      = "https://cran.rstudio.com/src/contrib/cowplot_0.8.0.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/cowplot"

    version('0.8.0', 'bcb19c72734d8eb5d73db393c1235c3d')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gtable', type=('build', 'run'))
    depends_on('r-plyr', type=('build', 'run'))
