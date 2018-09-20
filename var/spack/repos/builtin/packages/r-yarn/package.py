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


class RYarn(RPackage):
    """Expedite large RNA-Seq analyses using a combination of previously
       developed tools. YARN is meant to make it easier for the user in
       performing basic mis-annotation quality control, filtering, and
       condition-aware normalization. YARN leverages many Bioconductor tools
       and statistical techniques to account for the large heterogeneity and
       sparsity found in very large RNA-seq experiments."""

    homepage = "https://bioconductor.org/packages/yarn/"
    git      = "https://git.bioconductor.org/packages/yarn.git"

    version('1.2.0', commit='28af616ef8c27dcadf6568e276dea8465486a697')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biomart', type=('build', 'run'))
    depends_on('r-downloader', type=('build', 'run'))
    depends_on('r-edger', type=('build', 'run'))
    depends_on('r-gplots', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
    depends_on('r-matrixstats', type=('build', 'run'))
    depends_on('r-preprocesscore', type=('build', 'run'))
    depends_on('r-readr', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
    depends_on('r-quantro', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.2.0')
