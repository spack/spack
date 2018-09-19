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


class RSqldf(RPackage):
    """The sqldf() function is typically passed a single argument
    which is an SQL select statement where the table names are
    ordinary R data frame names. sqldf() transparently sets up a
    database, imports the data frames into that database, performs the
    SQL select or other statement and returns the result using a
    heuristic to determine which class to assign to each column of the
    returned data frame. The sqldf() or read.csv.sql() functions can
    also be used to read filtered files into R even if the original
    files are larger than R itself can handle. 'RSQLite', 'RH2',
    'RMySQL' and 'RPostgreSQL' backends are supported."""

    homepage = "https://cran.r-project.org/package=sqldf"
    url      = "https://cran.r-project.org/src/contrib/sqldf_0.4-11.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/sqldf"

    version('0.4-11', '85def6fe2418569370c24e53522d2c2d')

    depends_on('r-gsubfn', type=('build', 'run'))
    depends_on('r-proto', type=('build', 'run'))
    depends_on('r-rsqlite', type=('build', 'run'))
    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-chron', type=('build', 'run'))
