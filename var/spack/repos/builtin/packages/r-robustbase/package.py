# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRobustbase(RPackage):
    """"Essential" Robust Statistics. Tools allowing to analyze data
       with robust methods. This includes regression methodology
       including model selections and multivariate statistics where we
       strive to cover the book "Robust Statistics, Theory and Methods"
       by 'Maronna, Martin and Yohai'; Wiley 2006."""

    homepage = "https://robustbase.r-forge.r-project.org"
    url      = "https://cran.r-project.org/src/contrib/robustbase_0.92-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/robustbase"

    version('0.92-7', 'db3c8d12f9729b35bad17abf09e80b72')

    depends_on('r-deoptimr', type=('build', 'run'))
