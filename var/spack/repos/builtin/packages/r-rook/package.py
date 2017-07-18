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


class RRook(RPackage):
    """This package contains the Rook specification and convenience software
    for building and running Rook applications. To get started, be sure and
    read the 'Rook' help file first."""

    homepage = "https://CRAN.R-project.org/package=Rook"
    url      = "https://cran.r-project.org/src/contrib/Rook_1.1-1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/Rook"

    version('1.1-1', 'a2816dc6b4730a94e3148fcc92b595df')

    depends_on('r@2.13.0:')

    depends_on('r-brew', type=('build', 'run'))
