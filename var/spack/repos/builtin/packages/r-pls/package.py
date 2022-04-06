# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RPls(RPackage):
    """Partial Least Squares and Principal Component Regression.

    Multivariate regression methods Partial Least Squares Regression (PLSR),
    Principal Component Regression (PCR) and Canonical Powered Partial Least
    Squares (CPPLS)."""

    cran = "pls"

    version('2.8-0', sha256='eff3a92756ca34cdc1661fa36d2bf7fc8e9f4132d2f1ef9ed0105c83594618bf')
    version('2.7-3', sha256='8f1d960ab74f05fdd11c4c7a3d30ff9e263fc658f5690b67278ca7c045d0742c')
    version('2.7-1', sha256='f8fd817fc2aa046970c49a9a481489a3a2aef8b6f09293fb1f0218f00bfd834b')
    version('2.7-0', sha256='5ddc1249a14d69a7a39cc4ae81595ac8c0fbb1e46c911af67907baddeac35875')
    version('2.6-0', sha256='3d8708fb7f45863d3861fd231e06955e6750bcbe717e1ccfcc6d66d0cb4d4596')

    depends_on('r@2.10:', type=('build', 'run'))
