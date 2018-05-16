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


class RGeomorph(RPackage):
    """Read, manipulate, and digitize landmark data, generate shape variables
       via Procrustes analysis for points, curves and surfaces, perform shape
       analyses, and provide graphical depictions of shapes and patterns of
       shape variation."""

    homepage = "https://cran.r-project.org/package=geomorph"
    url      = "https://cran.r-project.org/src/contrib/geomorph_3.0.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/geomorph"

    version('3.0.5', '240e69fe260ca3ef4d84b4281d61396c')

    depends_on('r-rgl', type=('build', 'run'))
    depends_on('r-ape', type=('build', 'run'))
    depends_on('r-jpeg', type=('build', 'run'))
    depends_on('r-geiger', type=('build', 'run'))
    depends_on('r-matrix', type=('build', 'run'))
