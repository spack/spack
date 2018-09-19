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


class RBit64(RPackage):
    """Package 'bit64' provides serializable S3 atomic 64bit (signed)
    integers. These are useful for handling database keys and exact
    counting in +-2^63. WARNING: do not use them as replacement for 32bit
    integers, integer64 are not supported for subscripting by R-core and
    they have different semantics when combined with double, e.g.
    integer64 + double => integer64. Class integer64 can be used in vectors,
    matrices, arrays and data.frames. Methods are available for coercion
    from and to logicals, integers, doubles, characters and factors
    as well as many elementwise and summary functions. Many fast
    algorithmic operations such as 'match' and 'order' support
    inter- active data exploration
    and manipulation and optionally leverage caching."""

    homepage = "https://cran.rstudio.com/web/packages/bit64/index.html"
    url      = "https://cran.rstudio.com/src/contrib/bit64_0.9-7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/bit64"
    version('0.9-7', 'ac4bc39827338c552d329d3d4d2339c2')

    depends_on('r-bit', type=('build', 'run'))
