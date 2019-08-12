# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAffycoretools(RPackage):
    """Various wrapper functions that have been written to streamline
    the more common analyses that a core Biostatistician might see."""

    homepage = "https://www.bioconductor.org/packages/affycoretools/"
    git      = "https://git.bioconductor.org/packages/affycoretools.git"

    version('1.48.0', commit='e0d52e34eead1ac45d3e60c59efd940e4889eb99')

    depends_on('r@3.4.0:3.4.9', when='@1.48.0')
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-affy', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-gostats', type=('build', 'run'))
    depends_on('r-gcrma', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-annotationdbi', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-oligoclasses', type=('build', 'run'))
    depends_on('r-reportingtools', type=('build', 'run'))
    depends_on('r-hwriter', type=('build', 'run'))
    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
