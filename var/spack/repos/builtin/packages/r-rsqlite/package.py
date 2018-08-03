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


class RRsqlite(RPackage):
    """This package embeds the SQLite database engine in R and provides an
    interface compliant with the DBI package. The source for the SQLite engine
    (version 3.8.6) is included."""

    homepage = "https://cran.rstudio.com/web/packages/RSQLite/index.html"
    url      = "https://cran.r-project.org/src/contrib/RSQLite_2.0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/RSQLite"

    version('2.0', '63842410e78ccdfc52d4ee97992521d5')

    depends_on('r-dbi', type=('build', 'run'))
    depends_on('r-bit64', type=('build', 'run'))
    depends_on('r-blob', type=('build', 'run'))
    depends_on('r-memoise', type=('build', 'run'))
    depends_on('r-pkgconfig', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-bh', type=('build', 'run'))
    depends_on('r-plogr', type=('build', 'run'))
