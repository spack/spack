# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMitml(RPackage):
    """Provides tools for multiple imputation of missing data in multilevel
    modeling. Includes a user-friendly interface to the packages 'pan' and
    'jomo', and several functions for visualization, data management and the
    analysis of multiply imputed data sets."""

    homepage = "https://cran.r-project.org/package=mitml"
    url      = "https://cran.r-project.org/src/contrib/mitml_0.3-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mitml"
    version('0.3-5', '6f8659c33696915bf510241287b2a34d')

    depends_on('r-pan', type=('build', 'run'))
    depends_on('r-jomo', type=('build', 'run'))
    depends_on('r-haven', type=('build', 'run'))
