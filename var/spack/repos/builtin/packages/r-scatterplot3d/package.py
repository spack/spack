# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RScatterplot3d(RPackage):
    """scatterplot3d: 3D Scatter Plot"""

    homepage = "https://CRAN.R-project.org/package=scatterplot3d"
    url      = "https://cran.r-project.org/src/contrib/scatterplot3d_0.3-40.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/scatterplot3d"

    version('0.3-40', '67b9ab6131d244d7fc1db39dcc911dfe')

    depends_on('r@2.7.0:')
