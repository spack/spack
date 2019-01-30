# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVcd(RPackage):
    """Visualization techniques, data sets, summary and inference procedures
    aimed particularly at categorical data. Special emphasis is given to highly
    extensible grid graphics. The package was package was originally inspired
    by the book "Visualizing Categorical Data" by Michael Friendly and is now
    the main support package for a new book, "Discrete Data Analysis with R" by
    Michael Friendly and David Meyer (2015)."""

    homepage = "https://cran.r-project.org/package=vcd"
    url      = "https://cran.r-project.org/src/contrib/vcd_1.4-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/vcd"

    version('1.4-1', '7db150a77f173f85b69a1f86f73f8f02')

    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-colorspace', type=('build', 'run'))
    depends_on('r-lmtest', type=('build', 'run'))
