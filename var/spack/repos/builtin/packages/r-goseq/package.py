# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGoseq(RPackage):
    """Detects Gene Ontology and/or other user defined categories which are
       over/under represented in RNA-seq data"""

    homepage = "https://bioconductor.org/packages/release/bioc/html/goseq.html"
    git      = "https://git.bioconductor.org/packages/goseq.git"

    version('1.32.0', commit='32fcbe647eea17d7d0d7a262610811502c421d36')

    depends_on('r@3.5.0:3.5.9', when='@1.32.0:', type=('build', 'run'))
    depends_on('r-biasedurn', type=('build', 'run'))
    depends_on('r-genelendatabase@1.9.2:', type=('build', 'run'))
    depends_on('r-mgcv', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-go-db', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
