# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVegan(RPackage):
    """Ordination methods, diversity analysis and other functions for
    community and vegetation ecologists."""

    homepage = "https://github.com/vegandevs/vegan"
    url      = "https://cran.r-project.org/src/contrib/vegan_2.4-3.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/vegan"

    version('2.5-4', sha256='5116a440111fca49b5f95cfe888b180ff29a112e6301d5e2ac5cae0e628493e0')
    version('2.4-3', 'db17d4c4b9a4d421246abd5b36b00fec')

    depends_on('r@3.0:')
    depends_on('r-permute@0.9-0:', type=('build', 'run'))
