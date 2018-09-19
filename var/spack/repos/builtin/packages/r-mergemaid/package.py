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
