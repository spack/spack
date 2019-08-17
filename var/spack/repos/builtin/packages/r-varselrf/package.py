# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RVarselrf(RPackage):
    """Variable selection from random forests using both backwards variable
    elimination (for the selection of small sets of non-redundant variables)
    and selection based on the importance spectrum (somewhat similar to scree
    plots; for the selection of large, potentially highly-correlated variables)
    . Main applications in high-dimensional data (e.g., microarray data,
    and other genomics and proteomics applications)."""

    homepage = "http://ligarto.org/rdiaz/Software/Software.html"
    url      = "https://cloud.r-project.org/src/contrib/varSelRF_0.7-8.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/varSelRF"

    version('0.7-8', '103c460d0734bd38ae13496c839d3435')

    depends_on('r@2.0.0:', type=('build', 'run'))
    depends_on('r-randomforest', type=('build', 'run'))
