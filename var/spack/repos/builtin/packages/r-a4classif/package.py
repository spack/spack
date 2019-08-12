# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RA4classif(RPackage):
    """Automated Affymetrix Array Analysis Classification Package."""

    homepage = "https://www.bioconductor.org/packages/a4Classif/"
    git      = "https://git.bioconductor.org/packages/a4Classif.git"

    version('1.24.0', commit='ca06bf274c87a73fc12c29a6eea4b90289fe30b1')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-a4core', type=('build', 'run'))
    depends_on('r-a4preproc', type=('build', 'run'))
    depends_on('r-mlinterfaces', type=('build', 'run'))
    depends_on('r-rocr', type=('build', 'run'))
    depends_on('r-pamr', type=('build', 'run'))
    depends_on('r-glmnet', type=('build', 'run'))
    depends_on('r-varselrf', type=('build', 'run'))
