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


class RMitml(RPackage):
    """Provides tools for multiple imputation of missing data in multilevel
    modeling. Includes a user-friendly interface to the packages 'pan' and
    'jomo', and several functions for visualization, data management and the
    analysis of multiply imputed data sets."""

    homepage = "https://cran.r-project.org/package=mitml"
    url      = "https://cran.r-project.org/src/contrib/mitml_0.3-5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/mitml"
    version('0.3-5', '6f8659c33696915bf510241287b2a34d')

    depends_on('r-pan', type=('build', 'run'))
    depends_on('r-jomo', type=('build', 'run'))
    depends_on('r-haven', type=('build', 'run'))
