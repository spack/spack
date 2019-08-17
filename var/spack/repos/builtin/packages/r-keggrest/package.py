# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RKeggrest(RPackage):
    """This package provides functions and routines useful in the analysis
       of somatic signatures (cf. L. Alexandrov et al., Nature 2013). In
       particular, functions to perform a signature analysis with known
       signatures (LCD = linear combination decomposition) and a signature
       analysis on stratified mutational catalogue (SMC = stratify mutational
       catalogue) are provided."""

    homepage = "http://bioconductor.org/packages/KEGGREST"
    git      = "https://git.bioconductor.org/packages/KEGGREST.git"

    version('1.18.1', commit='f6e6f1987e4db9d977a75609fab0cb710be2e2e4')
    version('1.2.0',  commit='ed48de0def57a909894e237fa4731c4a052d8849')

    depends_on('r-httr', type=('build', 'run'))
    depends_on('r-png', type=('build', 'run'))
    depends_on('r-biostrings', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
    depends_on('r@3.4.3:3.4.9', when='@1.18.1')
