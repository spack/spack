# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RClass(RPackage):
    """Various functions for classification, including k-nearest neighbour,
    Learning Vector Quantization and Self-Organizing Maps."""

    homepage = "http://www.stats.ox.ac.uk/pub/MASS4/"
    url      = "https://cran.r-project.org/src/contrib/class_7.3-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/class"

    version('7.3-14', '6a21dd206fe4ea29c55faeb65fb2b71e')

    depends_on('r-mass', type=('build', 'run'))
