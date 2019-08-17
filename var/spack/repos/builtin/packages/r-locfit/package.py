# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLocfit(RPackage):
    """Local regression, likelihood and density estimation."""

    homepage = "https://cloud.r-project.org/package=locfit"
    url      = "https://cloud.r-project.org/src/contrib/locfit_1.5-9.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/locfit"

    version('1.5-9.1', '38af7791c9cda78e2804020e65ac7fb4')

    depends_on('r@2.0.1:', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
