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


class RPcamethods(RPackage):
    """Provides Bayesian PCA, Probabilistic PCA, Nipals PCA, Inverse
       Non-Linear PCA and the conventional SVD PCA. A cluster based method for
       missing value estimation is included for comparison. BPCA, PPCA and
       NipalsPCA may be used to perform PCA on incomplete data as well as for
       accurate missing value estimation. A set of methods for printing and
       plotting the results is also provided. All PCA methods make use of the
       same data structure (pcaRes) to provide a common interface to the PCA
       results. Initiated at the Max-Planck Institute for Molecular Plant
       Physiology, Golm, Germany."""

    homepage = "http://bioconductor.org/packages/pcaMethods/"
    git      = "https://git.bioconductor.org/packages/pcaMethods.git"

    version('1.68.0', commit='c8d7c93dcaf7ef728f3d089ae5d55771b320bdab')

    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-biocgenerics', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
    depends_on('r@3.4.0:3.4.9', when='@1.68.0')
