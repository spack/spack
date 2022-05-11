# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.package_defs import *


class RAplot(RPackage):
    """Decorate a 'ggplot' with Associated Information.

    For many times, we are not just aligning plots as what 'cowplot' and
    'patchwork' did. Users would like to align associated information that
    requires axes to be exactly matched in subplots, e.g. hierarchical
    clustering with a heatmap. This package provides utilities to aligns
    associated subplots to a main plot at different sides (left, right, top and
    bottom) with axes exactly matched."""

    cran = "aplot"

    version('0.1.2', sha256='899c4d101ddcedb1eba9803d78cf02288b63de25e2879add8add1165167509f0')

    depends_on('r-ggfun@0.0.4:', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-ggplotify', type=('build', 'run'))
    depends_on('r-patchwork', type=('build', 'run'))
    depends_on('r-magrittr', type=('build', 'run'))
    depends_on('r-yulab-utils', type=('build', 'run'))
