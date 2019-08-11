# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGeor(RPackage):
    """Geostatistical analysis including traditional, likelihood-based
       and Bayesian methods."""

    homepage = "https://cloud.r-project.org/package=geoR"
    url      = "https://cloud.r-project.org/src/contrib/geoR_1.7-5.2.1.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/geoR"

    version('1.7-5.2.1', 'a50f477bea1bec9070a4de01f69b831c')

    depends_on('r@2.10:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-sp', type=('build', 'run'))
    depends_on('r-splancs', type=('build', 'run'))
    depends_on('r-randomfields', type=('build', 'run'))
