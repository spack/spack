# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RScattermore(RPackage):
    """Scatterplots with More Points.

    C-based conversion of large scatterplot data to rasters. Speeds up plotting
    of data with millions of points."""

    cran = "scattermore"

    version('0.7', sha256='f36280197b8476314d6ce81a51c4ae737180b180204043d2937bc25bf3a5dfa2')

    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-scales', type=('build', 'run'))
