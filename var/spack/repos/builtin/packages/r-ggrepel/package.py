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


class RGgrepel(RPackage):
    """ggrepel: Repulsive Text and Label Geoms for 'ggplot2'"""

    homepage = "http://github.com/slowkow/ggrepel"
    url      = "https://cran.r-project.org/src/contrib/ggrepel_0.6.5.tar.gz"
    list_url = "https://cran.r-project.org/src/contrib/Archive/ggrepel"

    version('0.6.5', '7e2732cd4840efe2dc9e4bc689cf1ee5')

    depends_on('r@3.0.0:')
    depends_on('r-ggplot2@2.0.0:', type=('build', 'run'))
    depends_on('r-rcpp', type=('build', 'run'))
    depends_on('r-scales@0.3.0:', type=('build', 'run'))
