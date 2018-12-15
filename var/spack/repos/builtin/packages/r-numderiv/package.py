# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RNumderiv(RPackage):
    """Methods for calculating (usually) accurate numerical first and
    second order derivatives."""

    homepage = "https://cran.r-project.org/package=numDeriv"
    url      = "https://cran.r-project.org/src/contrib/numDeriv_2016.8-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/numDeriv"

    version('2016.8-1', '30e486298d5126d86560095be8e8aac1')

    depends_on('r@2.11.1:')
