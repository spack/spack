##############################################################################
# Copyright (c) 2013-2016, Lawrence Livermore National Security, LLC.
# Produced at the Lawrence Livermore National Laboratory.
#
# This file is part of Spack.
# Created by Todd Gamblin, tgamblin@llnl.gov, All rights reserved.
# LLNL-CODE-647188
#
# For details, see https://github.com/llnl/spack
# Please also see the LICENSE file for our notice and the LGPL.
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


class RSparsem(RPackage):
    """Some basic linear algebra functionality for sparse matrices is provided:
        including Cholesky decomposition and backsolving as well as standard R
        subsetting and Kronecker products."""

    homepage = "http://www.econ.uiuc.edu/~roger/research/sparse/sparse.html"
    url      = "https://cran.r-project.org/src/contrib/SparseM_1.74.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/SparseM"

    version('1.74', 'a16c9b7db172dfd2b7b6508c48e81a5d')
    version('1.7',  '7b5b0ab166a0929ef6dcfe1d97643601')
