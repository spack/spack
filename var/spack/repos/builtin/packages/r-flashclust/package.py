# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RFlashclust(RPackage):
    """flashClust: Implementation of optimal hierarchical clustering"""

    homepage = "https://cloud.r-project.org/package=flashClust"
    url      = "https://cloud.r-project.org/src/contrib/flashClust_1.01-2.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/flashClust"

    version('1.01-2', '23409aeeef98bf35d0b3d5dd755fdeff')

    depends_on('r@2.3.0:', type=('build', 'run'))
