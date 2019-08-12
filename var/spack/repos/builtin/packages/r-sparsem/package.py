# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

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
