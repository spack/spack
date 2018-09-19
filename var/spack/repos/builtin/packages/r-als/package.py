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


class RAls(RPackage):
    """Alternating least squares is often used to resolve components
    contributing to data with a bilinear structure; the basic
    technique may be extended to alternating constrained least squares.
    Commonly applied constraints include unimodality, non-negativity,
    and normalization of components. Several data matrices may be
    decomposed simultaneously by assuming that one of the two matrices
    in the bilinear decomposition is shared between datasets."""

    homepage = "https://cran.r-project.org/package=ALS"
    url      = "https://cran.rstudio.com/src/contrib/ALS_0.0.6.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/ALS"

    version('0.0.6', 'b72d97911e8ab7e4f8aed1a710b3d62d')

    depends_on('r-iso', type=('build', 'run'))
    depends_on('r-nnls', type=('build', 'run'))
