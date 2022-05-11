# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RBiasedurn(RPackage):
    """Biased Urn Model Distributions.

    Statistical models of biased sampling in the form of univariate and
    multivariate noncentral hypergeometric distributions, including Wallenius'
    noncentral hypergeometric distribution and Fisher's noncentral
    hypergeometric distribution (also called extended hypergeometric
    distribution). See vignette("UrnTheory") for explanation of these
    distributions."""

    cran = "BiasedUrn"

    version('1.07', sha256='2377c2e59d68e758a566452d7e07e88663ae61a182b9ee455d8b4269dda3228e')
