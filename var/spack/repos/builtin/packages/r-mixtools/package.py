# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMixtools(RPackage):
    """mixtools: Tools for Analyzing Finite Mixture Models

    Analyzes finite mixture models for various parametric and semiparametric
    settings."""

    homepage = "https://cloud.r-project.org/package=mixtools"
    url      = "https://cloud.r-project.org/src/contrib/mixtools_1.1.0.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/mixtools"

    version('1.1.0', 'c7d59110dd42964d40593a05b98acd5f')
    version('1.0.4', 'c0e6ec44d16ec8914797fb74a651d3e5')

    depends_on('r@3.2:', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r-segmented', type=('build', 'run'))
    depends_on('r-survival', type=('build', 'run'))
