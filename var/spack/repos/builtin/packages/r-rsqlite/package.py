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


class RRsqlite(RPackage):
    """This package embeds the SQLite database engine in R and provides an
    interface compliant with the DBI package. The source for the SQLite engine
    (version 3.8.6) is included."""

    homepage = "https://github.com/rstats-db/RSQLite"
    url      = "https://cran.r-project.org/src/contrib/RSQLite_1.0.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RSQLite"

    version('1.0.0', 'e6cbe2709612b687c13a10d30c7bad45')

    depends_on('r-dbi', type=('build', 'run'))
