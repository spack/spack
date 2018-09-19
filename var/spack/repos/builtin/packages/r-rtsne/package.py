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


class RRtsne(RPackage):
    """An R wrapper around the fast T-distributed Stochastic Neighbor
    Embedding implementation."""

    homepage = "https://CRAN.R-project.org/package=Rtsne"
    url      = "https://cran.r-project.org/src/contrib/Rtsne_0.13.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rtsne"

    version('0.13', 'ea1d2ef2bda16735bbf219ffda5b0661')
    version('0.11', '9a1eaa9b71d67cc27a55780e6e9df733')
    version('0.10', 'c587e1b76fdcea2629424f74c6e92340')

    depends_on('r@3.4.0:3.4.9')
    depends_on('r-rcpp', type=('build', 'run'))
