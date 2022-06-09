# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)


from spack import *


class RPaleotree(RPackage):
    """Paleontological and Phylogenetic Analyses of Evolution.

    Provides tools for transforming, a posteriori time-scaling, and modifying
    phylogenies containing extinct (i.e. fossil) lineages"""

    cran = "paleotree"

    version('3.3.25', sha256='aa64b9120075581229439227a12db776d052b03eb5f9721692a16a9402ac8712')
    version('3.3.0', sha256='f8f6b0228dd5290b251cad3a8626689442b5aa793d8f072c8c2c7813a063df90')
    version('3.1.3', sha256='4c1cc8a5e171cbbbd88f78914f86d5e6d144ae573816fbeeff2ab54a814ec614')

    depends_on('r@3.0.0:', type=('build', 'run'))
    depends_on('r-ape@4.1:', type=('build', 'run'))
    depends_on('r-phangorn@2.0.0:', type=('build', 'run'))
    depends_on('r-phytools@0.6-00:', type=('build', 'run'))
    depends_on('r-jsonlite', type=('build', 'run'), when='@3.3.0:')
    depends_on('r-png', type=('build', 'run'), when='@3.3.0:')
    depends_on('r-rcurl', type=('build', 'run'), when='@3.3.0:')
