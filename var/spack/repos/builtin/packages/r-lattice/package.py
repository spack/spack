# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
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
    url      = "https://cloud.r-project.org/src/contrib/lattice_0.20-35.tar.gz"
    list_url = "https://cloud.r-project.org/src/contrib/Archive/lattice"

    version('0.20-38', sha256='fdeb5e3e50dbbd9d3c5e2fa3eef865132b3eef30fbe53a10c24c7b7dfe5c0a2d')
    version('0.20-35', '07f1814623b3da6278ca61554ff7bfe6')
    version('0.20-34', 'c2a648b22d4206ae7526fb70b8e90fed')

    depends_on('r@3.0.0:', type=('build', 'run'))
