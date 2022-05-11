# Copyright 2013-2022 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack.util.package import *


class RClue(RPackage):
    """Cluster Ensembles."""

    cran = "clue"

    version('0.3-60', sha256='6d21ddfd0d621ed3bac861890c600884b6ed5ff7d2a36c9778b892636dbbef2a')
    version('0.3-58', sha256='2ab6662eaa1103a7b633477e8ebd266b262ed54fac6f9326b160067a2ded9ce7')
    version('0.3-57', sha256='6e369d07b464a9624209a06b5078bf988f01f7963076e946649d76aea0622d17')

    depends_on('r@3.2.0:', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
