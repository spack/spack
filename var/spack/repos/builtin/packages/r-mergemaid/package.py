# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMergemaid(RPackage):
    """The functions in this R extension are intended for cross-study
       comparison of gene expression array data. Required from the user is
       gene expression matrices, their corresponding gene-id vectors and
       other useful information, and they could be 'list','matrix', or
       'ExpressionSet'. The main function is 'mergeExprs' which transforms
       the input objects into data in the merged format, such that common
       genes in different datasets can be easily found. And the function
       'intcor' calculate the correlation coefficients. Other functions use
       the output from 'modelOutcome' to graphically display the results and
       cross-validate associations of gene expression data with survival."""

    homepage = "https://www.bioconductor.org/packages/MergeMaid/"
    git      = "https://git.bioconductor.org/packages/MergeMaid.git"

    version('2.48.0', commit='aee89c523fcafff4c166ff3db4fff90df16a1ed4')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@2.48.0')
