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


class RTmixclust(RPackage):
    """Implementation of a clustering method for time series gene expression
    data based on mixed-effects models with Gaussian variables and
    non-parametric cubic splines estimation. The method can robustly account
    for the high levels of noise present in typical gene expression time
    series datasets."""

    homepage = "https://bioconductor.org/packages/TMixClust/"
    git      = "https://git.bioconductor.org/packages/TMixClust.git"

    version('1.0.1', commit='0ac800210e3eb9da911767a80fb5582ab33c0cad')

    depends_on('r-gss', type=('build', 'run'))
    depends_on('r-mvtnorm', type=('build', 'run'))
    depends_on('r-zoo', type=('build', 'run'))
    depends_on('r-cluster', type=('build', 'run'))
    depends_on('r-biocparallel', type=('build', 'run'))
    depends_on('r-flexclust', type=('build', 'run'))
    depends_on('r-biobase', type=('build', 'run'))
    depends_on('r-spem', type=('build', 'run'))
    depends_on('r@3.4.3:3.4.9', when='@1.0.1')
