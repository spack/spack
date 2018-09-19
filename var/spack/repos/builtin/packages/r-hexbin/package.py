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


class RHexbin(RPackage):
    """Binning and plotting functions for hexagonal bins. Now uses and relies
    on grid graphics and formal (S4) classes and methods."""

    homepage = "http://github.com/edzer/hexbin"
    url      = "https://cran.r-project.org/src/contrib/hexbin_1.27.1.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/hexbin"

    version('1.27.1', '7590ed158f8a57a71901bf6ca26f81be')

    depends_on('r-lattice', type=('build', 'run'))
