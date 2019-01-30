# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RLattice(RPackage):
    """A powerful and elegant high-level data visualization system inspired by
    Trellis graphics, with an emphasis on multivariate data. Lattice is
    sufficient for typical graphics needs, and is also flexible enough to
    handle most nonstandard requirements. See ?Lattice for an introduction."""

    homepage = "http://lattice.r-forge.r-project.org/"
    url      = "https://cran.rstudio.com/src/contrib/lattice_0.20-35.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lattice"

    version('0.20-35', '07f1814623b3da6278ca61554ff7bfe6')
    version('0.20-34', 'c2a648b22d4206ae7526fb70b8e90fed')
