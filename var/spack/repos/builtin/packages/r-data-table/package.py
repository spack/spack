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


class RDataTable(RPackage):
    """Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins,
    fast add/modify/delete of columns by group using no copies at all, list
    columns and a fast file reader (fread). Offers a natural and flexible
    syntax, for faster development."""

    homepage = "https://github.com/Rdatatable/data.table/wiki"
    url      = "https://cran.r-project.org/src/contrib/data.table_1.10.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/data.table"

    version('1.10.0', 'f0e08dd5ba1b3f46c59dd1574fe497c1')
    version('1.9.6',  'b1c0c7cce490bdf42ab288541cc55372')

    depends_on('r@3.0.0:')
