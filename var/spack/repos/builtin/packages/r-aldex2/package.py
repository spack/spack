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


class RAldex2(RPackage):
    """A differential abundance analysis for the comparison of
    two or more conditions. For example, single-organism and
    meta-RNA-seq high-throughput sequencing assays, or of
    selected and unselected values from in-vitro sequence selections.
    Uses a Dirichlet-multinomial model to infer abundance from counts,
    that has been optimized for three or more experimental replicates.
    Infers sampling variation and calculates the expected false
    discovery rate given the biological and sampling variation
    using the Wilcox rank test or Welches t-test (aldex.ttest) or
    the glm and Kruskal Wallis tests (aldex.glm). Reports both P
    and fdr values calculated by the Benjamini Hochberg correction."""

    homepage = "http://bioconductor.org/packages/ALDEx2/"
    git      = "https://git.bioconductor.org/packages/ALDEx2.git"

    version('1.8.0', commit='24104824ca2402ad4f54fbf1ed9cee7fac2aaaf1')

    depends_on('r@3.4.0:3.4.9', when='@1.8.0')
    depends_on('r-s4vectors', type=('build', 'run'))
    depends_on('r-iranges', type=('build', 'run'))
    depends_on('r-genomicranges', type=('build', 'run'))
    depends_on('r-summarizedexperiment', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
