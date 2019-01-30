# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAgdex(RPackage):
    """A tool to evaluate agreement of differential expression
    for cross-species genomics."""

    homepage = "http://bioconductor.org/packages/AGDEX/"
    git      = "https://git.bioconductor.org/packages/AGDEX.git"

    version('1.24.0', commit='29c6bcfa6919a5c6d8bcb36b44e75145a60ce7b5')

    depends_on('r@3.4.0:3.4.9', when='@1.24.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
