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


class RLatticeextra(RPackage):
    """Building on the infrastructure provided by the lattice package,
    this package provides several new high-level functions and methods,
    as well as additional utilities such as panel and axis annotation
    functions."""

    homepage = "http://latticeextra.r-forge.r-project.org/"
    url      = "https://cran.rstudio.com/src/contrib/latticeExtra_0.6-28.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/latticeExtra"

    version('0.6-28', '771938f25d0983763369b48a1153b26c')

    depends_on('r-lattice', type=('build', 'run'))
    depends_on('r-rcolorbrewer', type=('build', 'run'))
