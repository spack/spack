# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RImpute(RPackage):
    """Imputation for microarray data (currently KNN only)."""

    homepage = "https://www.bioconductor.org/packages/impute/"
    git      = "https://git.bioconductor.org/packages/impute.git"

    version('1.50.1', commit='31d1cc141797afdc83743e1d95aab8a90ee19b71')

    depends_on('r@3.4.0:3.4.9', when='@1.50.1')
