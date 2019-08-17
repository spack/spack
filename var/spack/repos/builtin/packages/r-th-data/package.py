# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RThData(RPackage):
    """Contains data sets used in other packages Torsten Hothorn maintains."""

    homepage = "https://cran.r-project.org/package=TH.data"
    url      = "https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/TH.data"

    version('1.0-8', '2cc20acc8b470dff1202749b4bea55c4')
    version('1.0-7', '3e8b6b1a4699544f175215aed7039a94')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
