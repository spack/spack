# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cloud.r-project.org/src/contrib/robustbase_0.92-7.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/robustbase"

    version('0.93-5', sha256='bde564dbd52f04ab32f9f2f9dd09b9578f3ccd2541cf5f8ff430da42a55e7f56')
    version('0.93-4', sha256='ea9e03d484ef52ea805803477ffc48881e4c8c86ffda4eea56109f8b23f0a6e0')
    version('0.92-7', 'db3c8d12f9729b35bad17abf09e80b72')

    depends_on('r@3.0.2:', when='@:0.93-1.1', type=('build', 'run'))
    depends_on('r@3.1.0:', when='@0.93-2:', type=('build', 'run'))
    depends_on('r-deoptimr', type=('build', 'run'))
