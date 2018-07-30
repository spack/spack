##############################################################################
# Copyright (c) 2013-2018, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/spack/spack
# Please also see the NOTICE and LICENSE files for our notice and the LGPL.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License (as
# published by the Free Software Foundation) version 2.1, February 1999.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY OF
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the terms and
# conditions of the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA
##############################################################################
from spack import *


class RAmpliqueso(RPackage):
    """The package provides tools and reports for the analysis of
    amplicon sequencing panels, such as AmpliSeq."""

    homepage = "https://www.bioconductor.org/packages/ampliQueso/"
    git      = "https://git.bioconductor.org/packages/ampliQueso.git"

    version('1.14.0', commit='9a4c26ec594171279aba8ab7fe59c4a2ea09b06b')

    depends_on('r@3.4.0:3.4.9', when='@1.14.0')
    depends_on('r-samr', type=('build', 'run'))
    depends_on('r-deseq', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-xtable', type=('build', 'run'))
    depends_on('r-statmod', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-variantannotation', type=('build', 'run'))
    depends_on('r-foreach', type=('build', 'run'))
    depends_on('r-doparallel', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-knitr', type=('build', 'run'))
    depends_on('r-rnaseqmap', type=('build', 'run'))
