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


class RDeseq2(RPackage):
    """Estimate variance-mean dependence in count data from
    high-throughput sequencing assays and test for differential
    expression based on a model using the negative binomial
    distribution."""

    homepage = "https://www.bioconductor.org/packages/DESeq2/"
    git      = "https://git.bioconductor.org/packages/DESeq2.git"

    version('1.18.1', commit='ef65091d46436af68915124b752f5e1cc55e93a7')
    version('1.16.1', commit='0a815574382704a08ef8b906eceb0296f81cded5')

    depends_on('r@3.4.0:3.4.9', when='@1.16.1:')
    depends_on("r-rcpparmadillo", type=('build', 'run'))
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-genefilter', type=('build', 'run'))
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-geneplotter', type=('build', 'run'))
    depends_on('r-ggplot2', type=('build', 'run'))
    depends_on('r-hmisc', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
