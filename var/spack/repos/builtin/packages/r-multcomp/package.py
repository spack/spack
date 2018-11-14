# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMultcomp(RPackage):
    """Simultaneous tests and confidence intervals for general linear
    hypotheses in parametric models, including linear, generalized linear,
    linear mixed effects, and survival models. The package includes demos
    reproducing analyzes presented in the book "Multiple Comparisons Using R"
    (Bretz, Hothorn, Westfall, 2010, CRC Press)."""

    homepage = "http://multcomp.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/multcomp_1.4-6.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/multcomp"

    version('1.4-6', 'f1353ede2ed78b23859a7f1f1f9ebe88')

    depends_on('r-mvtnorm@1.0-3:', type=('build', 'run'))
    depends_on('r-survival@2.39-4:', type=('build', 'run'))
    depends_on('r-th-data@1.0-2:', type=('build', 'run'))
    depends_on('r-sandwich@2.3-0:', type=('build', 'run'))
    depends_on('r-codetools', type=('build', 'run'))
