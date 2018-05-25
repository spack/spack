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


class RSom(RPackage):
    """Self-Organizing Map (with application in gene clustering)."""

    homepage = "https://cran.r-project.org/web/packages/som/index.html"
    url      = "https://cran.r-project.org/src/contrib/som_0.3-5.1.tar.gz"
    list_url = "https://cran.rstudio.com/src/contrib/Archive/som"

    version('0.3-5.1', '802a5a80902579354ce3420faeeeb756')
    version('0.3-5', '72717499794c7aa945a768b742af8895')
    version('0.3-4', '1e25572e446409f5e32c5da5f1af98e6')
    version('0.3-3', 'd4ac444be24f71d08b99974c2f4b96e5')
    version('0.3-2', '4ce28f46df68fbb73905711ba2416fac')

    depends_on('r@3.4.0:3.4.9')
