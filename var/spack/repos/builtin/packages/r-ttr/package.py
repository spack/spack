# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RTtr(RPackage):
    """Functions and data to construct technical trading rules with R."""

    homepage = "https://github.com/joshuaulrich/TTR"
    url      = "https://cran.r-project.org/src/contrib/TTR_0.23-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/TTR"

    version('0.23-1', '35f693ac0d97e8ec742ebea2da222986')

    depends_on('r-xts', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
