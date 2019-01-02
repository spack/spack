# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RCategory(RPackage):
    """A collection of tools for performing category analysis."""

    homepage = "https://www.bioconductor.org/packages/Category/"
    git      = "https://git.bioconductor.org/packages/Category.git"

    version('2.42.1', commit='382c817a2371671a72f8f949dfb4050361ebabcd')

    depends_on('r@3.4.0:3.4.9', when='@2.42.1')
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-graph', type=('build', 'run'))
    depends_on('r-rbgl', type=('build', 'run'))
    depends_on('r-gseabase', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-annotate', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
