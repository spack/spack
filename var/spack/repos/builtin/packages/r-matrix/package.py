# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RMatrix(RPackage):
    """Classes and methods for dense and sparse matrices and operations on them
    using 'LAPACK' and 'SuiteSparse'."""

    homepage = "http://matrix.r-forge.r-project.org/"
    url      = "https://cran.rstudio.com/src/contrib/Matrix_1.2-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Matrix"

    version('1.2-14', 'b2babcf1515625196b75592c9b345bba')
    version('1.2-12', '0ade6e374716f08650cc8b8da99a313c')
    version('1.2-11', 'b7d2a639aa52228dfde7c3c3ee68b38e')
    version('1.2-8', '4a6406666bf97d3ec6b698eea5d9c0f5')
    version('1.2-6', 'f545307fb1284861e9266c4e9712c55e')

    depends_on('r-lattice', type=('build', 'run'))
