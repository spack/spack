# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMnormt(RPackage):
    """Functions are provided for computing the density and the distribution
       function of multivariate normal and "t" random variables, and for
       generating random vectors sampled from these distributions.
       Probabilities are computed via non-Monte Carlo methods; different
       routines are used in the case d=1, d=2, d>2, if d denotes the number
       of dimensions."""

    homepage = "http://azzalini.stat.unipd.it/SW/Pkg-mnormt"
    url      = "https://cloud.r-project.org/src/contrib/mnormt_1.5-5.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mnormt"

    version('1.5-5', '19b5be2e9ed33b92d7a716bfcca6b2c7')

    depends_on('r@2.2.0:', type=('build', 'run'))
