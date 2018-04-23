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


class RSegmented(RPackage):
    """Given a regression model, segmented 'updates' the model by adding
    one or more segmented (i.e., piecewise-linear) relationships. Several
    variables with multiple breakpoints are allowed."""

    homepage = "https://CRAN.R-project.org/package=segmented"
    url      = "https://cran.r-project.org/src/contrib/segmented_0.5-1.4.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/segmented"

    version('0.5-2.2', '1511ec365aea289d5f0a574f6d10d2d6')
    version('0.5-1.4', 'f9d76ea9e22ef5f40aa126b697351cae')
