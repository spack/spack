# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
