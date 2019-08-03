# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPls(RPackage):
    """Multivariate regression methods Partial Least Squares Regression (PLSR),
    Principal Component Regression (PCR) and Canonical Powered Partial Least
    Squares (CPPLS)."""

    homepage = "https://cloud.r-project.org/package=pls"
    url      = "https://cloud.r-project.org/src/contrib/pls_2.6-0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/pls"

    version('2.7-0', sha256='5ddc1249a14d69a7a39cc4ae81595ac8c0fbb1e46c911af67907baddeac35875')
    version('2.6-0', '04e02e8e46d983c5ed53c1f952b329df')

    depends_on('r@2.10:')
