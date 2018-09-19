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


class RLsei(RPackage):
    """It contains functions that solve least squares linear regression
       problems under linear equality/inequality constraints. Functions for
       solving quadratic programming problems are also available, which
       transform such problems into least squares ones first. It is developed
       based on the 'Fortran' program of Lawson and Hanson (1974, 1995), which
       is public domain and available at
       <http://www.netlib.org/lawson-hanson>."""

    homepage = "https://cran.r-project.org/package=lsei"
    url      = "https://cran.rstudio.com/src/contrib/lsei_1.2-0.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/lsei"

    version('1.2-0', '18a9322d7a79ecb86b8788645c4b7e3c')
