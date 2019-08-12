# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RViridislite(RPackage):
    """viridisLite: Default Color Maps from 'matplotlib' (Lite Version)"""

    homepage = "https://github.com/sjmgarnier/viridisLite"
    url      = "https://cran.r-project.org/src/contrib/viridisLite_0.2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/viridisLite"

    version('0.2.0', '04a04415cf651a2b5f964b261896c0fb')

    depends_on('r@2.1.0:')
