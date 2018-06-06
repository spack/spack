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


class RSplitstackshape(RPackage):
    """Stack and Reshape Datasets After Splitting Concatenated Values.

    Online data collection tools like Google Forms often export
    multiple-response questions with data concatenated in cells. The
    concat.split (cSplit) family of functions splits such data into
    separate cells. The package also includes functions to stack groups
    of columns and to reshape wide data, even when the data are
    "unbalanced" something which reshape (from base R) does not handle,
    and which melt and dcast from reshape2 do not easily handle.
    """

    homepage = "http://github.com/mrdwab/splitstackshape"
    url      = "https://cran.r-project.org/src/contrib/splitstackshape_1.4.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/splitstackshape"

    version('1.4.4', '54d2554fe92dfc4670a000b45baacc28')

    depends_on('r-data-table@1.9.4:', type=('build', 'run'))
    depends_on('r@2.10:', type=('build', 'run'))
