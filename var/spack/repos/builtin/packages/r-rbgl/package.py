# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RRbgl(RPackage):
    """A fairly extensive and comprehensive interface to the graph
    algorithms contained in the BOOST library."""

    homepage = "https://www.bioconductor.org/packages/RBGL/"
    git      = "https://git.bioconductor.org/packages/RBGL.git"

    version('1.60.0', commit='ef24c17c411659b8f030602bd9781c534d6ec93b')
    version('1.52.0', commit='93e8fcfafec8f1cd5638fe30dc0f9506d15b49c0')

    depends_on('r@3.4.0:3.4.9', when='@1.52.0')
    depends_on('r@3.6.0:', when='@1.60.0', type=('build', 'run'))
    depends_on('r-bh', when='@1.60.0', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
