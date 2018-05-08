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
