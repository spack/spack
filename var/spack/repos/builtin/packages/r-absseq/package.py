# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RAbsseq(RPackage):
    """Inferring differential expression genes by absolute counts
    difference between two groups, utilizing Negative binomial
    distribution and moderating fold-change according to heterogeneity
    of dispersion across expression level."""

    homepage = "https://www.bioconductor.org/packages/ABSSeq/"
    git      = "https://git.bioconductor.org/packages/ABSSeq.git"

    version('1.22.8', commit='a67ba49bc156a4522092519644f3ec83d58ebd6a')

    depends_on('r@3.4.0:3.4.9', when='@1.22.8')
    depends_on('r-locfit', type=('build', 'run'))
    depends_on('r-limma', type=('build', 'run'))
