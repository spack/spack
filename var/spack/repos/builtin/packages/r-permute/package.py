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


class RPermute(RPackage):
    """A set of restricted permutation designs for freely exchangeable, line
    transects (time series), and spatial grid designs plus permutation of
    blocks (groups of samples) is provided. 'permute' also allows split-plot
    designs, in which the whole-plots or split-plots or both can be
    freely-exchangeable or one of the restricted designs. The 'permute'
    package is modelled after the permutation schemes of 'Canoco 3.1'
    (and later) by Cajo ter Braak."""

    homepage = "https://github.com/gavinsimpson/permute"
    url      = "https://cran.r-project.org/src/contrib/permute_0.9-4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/permute"

    version('0.9-4', '569fc2442d72a1e3b7e2d456019674c9')

    depends_on('r@2.14:')
