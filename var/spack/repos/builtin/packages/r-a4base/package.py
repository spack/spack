# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4base(RPackage):
    """Automated Affymetrix Array Analysis."""

    homepage = "https://www.bioconductor.org/packages/a4Base/"
    git      = "https://git.bioconductor.org/packages/a4Base.git"

    version('1.24.0', commit='f674afe424a508df2c8ee6c87a06fbd4aa410ef6')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-annaffy', type=('build', 'run'))
    depends_on('r-mpm', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-multtest', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-a4preproc', type=('build', 'run'))
    depends_on('r-a4core', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
