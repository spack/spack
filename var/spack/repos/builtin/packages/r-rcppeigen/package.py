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


class RRcppeigen(RPackage):
    """R and 'Eigen' integration using 'Rcpp'. 'Eigen' is a C++ template
    library for linear algebra: matrices, vectors, numerical solvers and
    related algorithms. It supports dense and sparse matrices on integer,
    floating point and complex numbers, decompositions of such matrices, and
    solutions of linear systems. Its performance on many algorithms is
    comparable with some of the best implementations based on 'Lapack' and
    level-3 'BLAS'. The 'RcppEigen' package includes the header files from the
    'Eigen' C++ template library (currently version 3.2.8). Thus users do not
    need to install 'Eigen' itself in order to use 'RcppEigen'. Since version
    3.1.1, 'Eigen' is licensed under the Mozilla Public License (version 2);
    earlier version were licensed under the GNU LGPL version 3 or later.
    'RcppEigen' (the 'Rcpp' bindings/bridge to 'Eigen') is licensed under the
    GNU GPL version 2 or later, as is the rest of 'Rcpp'."""

    homepage = "http://eigen.tuxfamily.org/"
    url      = "https://cran.r-project.org/src/contrib/RcppEigen_0.3.2.9.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RcppEigen"

    version('0.3.2.9.0', '14a7786882a5d9862d53c4b2217df318')
    version('0.3.2.8.1', '4146e06e4fdf7f4d08db7839069d479f')

    depends_on('r-matrix', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
