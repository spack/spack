# Copyright 2013-2018 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class RDataTable(RPackage):
    """Fast aggregation of large data (e.g. 100GB in RAM), fast ordered joins,
    fast add/modify/delete of columns by group using no copies at all, list
    columns and a fast file reader (fread). Offers a natural and flexible
    syntax, for faster development."""

    homepage = "https://github.com/Rdatatable/data.table/wiki"
    url      = "https://cran.r-project.org/src/contrib/data.table_1.10.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/data.table"

    version('1.10.4-3', '081da241d06f30ae4a2bc60efb409893')
    version('1.10.4-2', '4a2d3541f241088d0979522b4083a765')
    version('1.10.0', 'f0e08dd5ba1b3f46c59dd1574fe497c1')
    version('1.9.6',  'b1c0c7cce490bdf42ab288541cc55372')

    depends_on('r@3.0.0:')
