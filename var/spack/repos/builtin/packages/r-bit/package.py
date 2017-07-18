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


class RBit(RPackage):
    """bitmapped vectors of booleans (no NAs), coercion from and to logicals,
    integers and integer subscripts; fast boolean operators and fast summary
    statistics. With 'bit' vectors you can store true binary booleans
    {FALSE,TRUE} at the expense of 1 bit only, on a 32 bit architecture this
    means factor 32 less RAM and ~ factor 32 more speed on boolean operations.
    Due to overhead of R calls, actual speed gain depends on the size of the
    vector: expect gains for vectors of size > 10000 elements. Even for
    one-time boolean operations it can pay-off to convert to bit, the pay-off
    is obvious, when such components are used more than once. Reading from
    and writing to bit is approximately as fast as accessing standard logicals
    - mostly due to R's time for memory allocation. The package allows to work
    with pre-allocated memory for return values by calling .Call() directly:
    when evaluating the speed of C-access with pre-allocated vector memory,
    coping from bit to logical requires only 70% of the time for copying from
    logical to logical; and copying from logical to bit comes at a performance
    penalty of 150%. the package now contains further classes for representing
    logical selections: 'bitwhich' for very skewed selections and 'ri' for
    selecting ranges of values for chunked processing. All three index classes
    can be used for subsetting 'ff' objects (ff-2.1-0 and higher)."""

    homepage = "http://ff.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/bit_1.1-12.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bit"

    version('1.1-12', 'c4473017beb93f151a8e672e4d5747af')

    depends_on('r@2.9.2:', type=('build', 'run'))
