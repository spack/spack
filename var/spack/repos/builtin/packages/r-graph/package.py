# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RGraph(RPackage):
    """A package that implements some simple graph handling capabilities."""

    homepage = "https://www.bioconductor.org/packages/graph/"
    git      = "https://git.bioconductor.org/packages/graph.git"

    version('1.54.0', commit='2a8b08520096241620421078fc1098f4569c7301')

    depends_on('r@2.10:', type=('build', 'run'), when='@1.54.0')
    depends_on('r-biocgenerics', type=('build', 'run'))
