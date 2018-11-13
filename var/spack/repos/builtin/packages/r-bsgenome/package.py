# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RBsgenome(RPackage):
    """Infrastructure shared by all the Biostrings-based genome data
       packages."""

    homepage = "https://www.bioconductor.org/packages/BSgenome/"
    git      = "https://git.bioconductor.org/packages/BSgenome.git"

    version('1.46.0', commit='bdfbd6d09820993585b8231ddea5e11c99008dc5')
    version('1.44.2', commit='105b00588a758d5ec7c347a7dff2756aea4516a0')

    depends_on('r-biocgenerics@0.13.8:', type=('build', 'run'))
    depends_on('r-s4vectors@0.9.36:', type=('build', 'run'))
    depends_on('r-iranges@2.1.33:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-iranges@2.11.16:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-genomeinfodb@1.11.4:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-genomeinfodb@1.13.1:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-genomicranges@1.27.6:', type=('build', 'run'), when='@1.44.2')
    depends_on('r-genomicranges@1.29.14:', type=('build', 'run'), when='@1.46.0')
    depends_on('r-biostrings@2.35.3:', type=('build', 'run'))
    depends_on('r-rtracklayer@1.25.8:', type=('build', 'run'))
    depends_on('r-rsamtools', type=('build', 'run'))
    depends_on('r-xvector', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.44.2:')
