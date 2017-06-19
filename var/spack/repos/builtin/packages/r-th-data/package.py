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


class RThData(RPackage):
    """Contains data sets used in other packages Torsten Hothorn maintains."""

    homepage = "https://cran.r-project.org/package=TH.data"
    url      = "https://cran.r-project.org/src/contrib/TH.data_1.0-8.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/TH.data"

    version('1.0-8', '2cc20acc8b470dff1202749b4bea55c4')
    version('1.0-7', '3e8b6b1a4699544f175215aed7039a94')

    depends_on('r-survival', type=('build', 'run'))
    depends_on('r-mass', type=('build', 'run'))
