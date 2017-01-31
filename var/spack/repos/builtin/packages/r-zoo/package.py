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


class RZoo(RPackage):
    """An S3 class with methods for totally ordered indexed observations. It is
    particularly aimed at irregular time series of numeric vectors/matrices and
    factors. zoo's key design goals are independence of a particular
    index/date/time class and consistency with ts and base R by providing
    methods to extend standard generics."""

    homepage = "http://zoo.r-forge.r-project.org/"
    url      = "https://cran.r-project.org/src/contrib/zoo_1.7-14.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/zoo"

    version('1.7-14', '8c577a7c1e535c899ab14177b1039c32')
    version('1.7-13', '99521dfa4c668e692720cefcc5a1bf30')

    depends_on('r-lattice', type=('build', 'run'))
