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


class RDbi(RPackage):
    """A database interface definition for communication between R and
    relational database management systems. All classes in this package are
    virtual and need to be extended by the various R/DBMS implementations."""

    homepage = "http://rstats-db.github.io/DBI"
    url      = "https://cran.rstudio.com/src/contrib/DBI_0.7.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/DBI"
    version('0.4-1', 'c7ee8f1c5037c2284e99c62698d0f087')
    version('0.7', '66065dd687d758b72d638adb6a8cab2e')
