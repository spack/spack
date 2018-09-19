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


class RAlsace(RPackage):
    """Alternating Least Squares (or Multivariate Curve Resolution)
    for analytical chemical data, in particular hyphenated data where
    the first direction is a retention time axis, and the second a
    spectral axis. Package builds on the basic als function from the
    ALS package and adds functionality for high-throughput analysis,
    including definition of time windows, clustering of profiles,
    retention time correction, etcetera."""

    homepage = "https://www.bioconductor.org/packages/alsace/"
    git      = "https://git.bioconductor.org/packages/alsace.git"

    version('1.12.0', commit='1364c65bbff05786d05c02799fd44fd57748fae3')

    depends_on('r-als', type=('build', 'run'))
    depends_on('r-ptw', type=('build', 'run'))
