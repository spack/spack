# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPbkrtest(RPackage):
    """Test in mixed effects models. Attention is on mixed effects models as
    implemented in the 'lme4' package. This package implements a parametric
    bootstrap test and a Kenward Roger modification of F-tests for linear mixed
    effects models and a parametric bootstrap test for generalized linear mixed
    models."""

    homepage = "http://people.math.aau.dk/~sorenh/software/pbkrtest/"
    url      = "https://cloud.r-project.org/src/contrib/pbkrtest_0.4-6.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pbkrtest"

    version('0.4-7', sha256='5cbb03ad2b2468720a5a610a0ebda48ac08119a34fca77810a85f554225c23ea')
    version('0.4-6', '0a7d9ff83b8d131af9b2335f35781ef9')
    version('0.4-4', '5e54b1b1b35413dd1d24ef15735ec645')

    depends_on('r@3.0.2:', when='@:0.4-5', type=('build', 'run'))
    depends_on('r@3.2.3:', when='@0.4-6:', type=('build', 'run'))
    depends_on('r-lme4@1.1.10:', type=('build', 'run'))
    depends_on('r-matrix@1.2.3:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
